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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list_create(request):
    """List all events or create a new event"""
    
    if request.method == 'GET':
        try:
            events = Event.objects.all().order_by('-created_at')
            serializer = EventSerializer(events, many=True)
            
            return Response({
                'events': serializer.data,
                'count': len(events)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to fetch events: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        serializer = EventCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                event = serializer.save()
                response_serializer = EventSerializer(event)
                
                return Response({
                    'message': 'Event created successfully',
                    'event': response_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'error': f'Failed to create event: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'error': 'Invalid data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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
