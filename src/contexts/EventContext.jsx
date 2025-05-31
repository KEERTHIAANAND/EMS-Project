
    import React, { createContext, useContext, useState, useEffect } from 'react';
    import { useToast } from '@/components/ui/use-toast.jsx';

    const EventContext = createContext();

    export const useEvents = () => useContext(EventContext);

    export const EventProvider = ({ children }) => {
      const [events, setEvents] = useState([]);
      const [loading, setLoading] = useState(false);
      const { toast } = useToast();

      // Get auth token
      const getAuthToken = () => {
        return localStorage.getItem('token');
      };

      // Check if user is authenticated
      const isAuthenticated = () => {
        const token = getAuthToken();
        const isAuth = localStorage.getItem('isAuthenticated') === 'true';
        return token && isAuth;
      };

      // Fetch events from MongoDB API
      const fetchEvents = async () => {
        if (!isAuthenticated()) {
          console.log('User not authenticated, skipping event fetch');
          return;
        }

        setLoading(true);
        try {
          const response = await fetch('http://localhost:8000/api/events/', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${getAuthToken()}`,
              'Content-Type': 'application/json',
            },
          });

          const data = await response.json();

          if (response.ok) {
            setEvents(data.events || []);
          } else {
            console.error('Failed to fetch events:', data.error);
            if (response.status === 503) {
              toast({
                title: "Database Connection Issue",
                description: "Unable to connect to database. Please try again later.",
                variant: "destructive",
              });
            }
          }
        } catch (error) {
          console.error('Network error fetching events:', error);
          toast({
            title: "Network Error",
            description: "Unable to fetch events. Please check your connection.",
            variant: "destructive",
          });
        } finally {
          setLoading(false);
        }
      };

      // Add event to MongoDB API
      const addEvent = async (event) => {
        if (!isAuthenticated()) {
          toast({
            title: "Authentication Required",
            description: "Please login to create events.",
            variant: "destructive",
          });
          return false;
        }

        setLoading(true);
        try {
          const response = await fetch('http://localhost:8000/api/events/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${getAuthToken()}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(event),
          });

          const data = await response.json();

          if (response.ok) {
            // Add the new event to local state
            setEvents((prevEvents) => [...prevEvents, data.event]);

            toast({
              title: "Event Created!",
              description: data.message || `"${event.name}" has been successfully created in MongoDB Atlas.`,
              variant: "success",
            });
            return true;
          } else {
            if (response.status === 503) {
              toast({
                title: "Database Connection Failed",
                description: "Unable to connect to database. Please ensure MongoDB Atlas is accessible.",
                variant: "destructive",
              });
            } else {
              toast({
                title: "Event Creation Failed",
                description: data.error || "Failed to create event. Please try again.",
                variant: "destructive",
              });
            }
            return false;
          }
        } catch (error) {
          console.error('Network error creating event:', error);
          toast({
            title: "Network Error",
            description: "Unable to create event. Please check your connection.",
            variant: "destructive",
          });
          return false;
        } finally {
          setLoading(false);
        }
      };

      const updateEvent = (updatedEvent) => {
        setEvents((prevEvents) =>
          prevEvents.map((event) =>
            event.id === updatedEvent.id ? updatedEvent : event
          )
        );
        toast({
          title: "Event Updated!",
          description: `"${updatedEvent.name}" has been successfully updated.`,
          variant: "success",
        });
      };

      const deleteEvent = (eventId) => {
        const eventToDelete = events.find(event => event.id === eventId);
        setEvents((prevEvents) =>
          prevEvents.filter((event) => event.id !== eventId)
        );
        if (eventToDelete) {
          toast({
            title: "Event Deleted",
            description: `"${eventToDelete.name}" has been removed.`,
            variant: "destructive",
          });
        }
      };

      const getEventById = (eventId) => {
        return events.find((event) => event.id === eventId);
      };

      const addRsvp = (eventId, rsvpDetails) => {
        setEvents(prevEvents => prevEvents.map(event => {
          if (event.id === eventId) {
            return { ...event, rsvps: [...(event.rsvps || []), { ...rsvpDetails, id: Date.now().toString() }] };
          }
          return event;
        }));
        toast({
          title: "RSVP Confirmed!",
          description: "Your registration for the event is confirmed.",
          variant: "success",
        });
      };


      // Fetch events on component mount
      useEffect(() => {
        fetchEvents();
      }, []);

      return (
        <EventContext.Provider value={{
          events,
          loading,
          addEvent,
          updateEvent,
          deleteEvent,
          getEventById,
          addRsvp,
          fetchEvents,
          isAuthenticated
        }}>
          {children}
        </EventContext.Provider>
      );
    };
