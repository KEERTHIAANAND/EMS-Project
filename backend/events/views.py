"""
Event views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer, EventCreateSerializer, RSVPCreateSerializer
from mongoengine.errors import DoesNotExist, ValidationError
from bson import ObjectId
from .fallback_events import (
    is_mongodb_available,
    create_fallback_event,
    get_all_fallback_events,
    migrate_fallback_to_mongodb
)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone to view events, but check auth for creation
def event_list_create(request):
    """List all events or create a new event"""

    if request.method == 'GET':
        # Always get fallback events first (guaranteed to work)
        try:
            fallback_events = get_all_fallback_events()
            mongodb_events = []

            # Try to get MongoDB events if available
            try:
                if is_mongodb_available():
                    # Try to migrate any fallback events first
                    migrate_fallback_to_mongodb()

                    # Fetch events from MongoDB
                    mongo_events = Event.objects.all().order_by('-created_at')
                    mongodb_events = [event.to_dict() for event in mongo_events]
                    print(f"Successfully fetched {len(mongodb_events)} events from MongoDB")
            except Exception as mongo_error:
                print(f"MongoDB fetch failed (using fallback): {mongo_error}")

            # Combine events (prefer MongoDB if available, otherwise use fallback)
            if mongodb_events:
                events_data = mongodb_events
                storage_info = "MongoDB Atlas"
                message = "Events fetched successfully from MongoDB Atlas"
            else:
                events_data = fallback_events
                storage_info = "Fallback Storage (MongoDB unavailable)"
                message = "Events fetched from local storage (MongoDB unavailable)"

            return Response({
                'message': message,
                'events': events_data,
                'count': len(events_data),
                'storage': storage_info,
                'fallback_count': len(fallback_events),
                'mongodb_count': len(mongodb_events)
            }, status=status.HTTP_200_OK)

        except Exception as error:
            print(f"Event listing error: {error}")
            return Response({
                'message': 'No events available',
                'events': [],
                'count': 0,
                'storage': 'Error',
                'error': 'Failed to fetch events'
            }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Check authentication for event creation
        if not request.user or not hasattr(request.user, 'is_authenticated') or not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required to create events. Please login first.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Get data from request
            name = request.data.get('name')
            description = request.data.get('description')
            date = request.data.get('date')
            time = request.data.get('time')
            location = request.data.get('location')

            # Basic validation
            if not all([name, description, date, time, location]):
                return Response({
                    'error': 'All fields are required (name, description, date, time, location)'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate date format (YYYY-MM-DD)
            try:
                from datetime import datetime
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return Response({
                    'error': 'Invalid date format. Please use YYYY-MM-DD format.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate time format (HH:MM)
            try:
                datetime.strptime(time, '%H:%M')
            except ValueError:
                return Response({
                    'error': 'Invalid time format. Please use HH:MM format.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Always try fallback first for reliability, then try MongoDB
            authenticated_user = request.user

            # Try to save in MongoDB first
            try:
                if is_mongodb_available():
                    # Create event in MongoDB Atlas
                    mongodb_event = Event(
                        name=name,
                        description=description,
                        date=date,
                        time=time,
                        location=location,
                        created_by=authenticated_user
                    )
                    mongodb_event.save()

                    # Serialize the MongoDB event for response
                    from .serializers import EventSerializer
                    serializer = EventSerializer(mongodb_event)

                    print(f"Event successfully saved to MongoDB Atlas: {name}")

                    return Response({
                        'message': 'Event created successfully! Stored in MongoDB Atlas',
                        'event': serializer.data,
                        'storage': 'MongoDB Atlas',
                        'mongodb_saved': True
                    }, status=status.HTTP_201_CREATED)

                else:
                    # MongoDB not available, use fallback storage
                    fallback_event = create_fallback_event(
                        name=name,
                        description=description,
                        date=date,
                        time=time,
                        location=location,
                        user=authenticated_user
                    )

                    print(f"Event saved to fallback storage (MongoDB unavailable): {name}")

                    return Response({
                        'message': 'Event created successfully! Stored in fallback storage',
                        'event': fallback_event.to_dict(),
                        'storage': 'Fallback Storage (MongoDB unavailable)',
                        'mongodb_saved': False
                    }, status=status.HTTP_201_CREATED)

            except Exception as creation_error:
                print(f"Event creation error: {creation_error}")
                return Response({
                    'error': 'Failed to create event. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(f"Unexpected error during event creation: {e}")
            return Response({
                'error': 'Event creation failed. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, event_id):
    """Get, update, or delete a specific event"""

    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(event_id):
            return Response({
                'error': 'Invalid event ID format'
            }, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.get(id=event_id)

    except DoesNotExist:
        return Response({
            'error': 'Event not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        try:
            serializer = EventSerializer(event)
            return Response({
                'event': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'Failed to fetch event: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        # Check if user is the creator or admin
        if event.created_by.id != request.user.id and not request.user.is_admin:
            return Response({
                'error': 'Permission denied. You can only edit your own events.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = EventCreateSerializer(event, data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                updated_event = serializer.save()
                response_serializer = EventSerializer(updated_event)

                return Response({
                    'message': 'Event updated successfully',
                    'event': response_serializer.data
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'error': f'Failed to update event: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Check if user is the creator or admin
        if event.created_by.id != request.user.id and not request.user.is_admin:
            return Response({
                'error': 'Permission denied. You can only delete your own events.'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            event.delete()
            return Response({
                'message': 'Event deleted successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'Failed to delete event: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to RSVP
def event_rsvp(request, event_id):
    """Add RSVP to an event"""

    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(event_id):
            return Response({
                'error': 'Invalid event ID format'
            }, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.get(id=event_id)

    except DoesNotExist:
        return Response({
            'error': 'Event not found'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = RSVPCreateSerializer(data=request.data)

    if serializer.is_valid():
        try:
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']

            success, message = event.add_rsvp(name, email)

            if success:
                response_serializer = EventSerializer(event)
                return Response({
                    'message': message,
                    'event': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': message
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': f'Failed to add RSVP: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_events(request):
    """Get events created by the current user"""

    try:
        events = Event.objects(created_by=request.user).order_by('-created_at')
        serializer = EventSerializer(events, many=True)

        return Response({
            'events': serializer.data,
            'count': len(events)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Failed to fetch user events: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
