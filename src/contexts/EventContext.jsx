
    import React, { createContext, useContext } from 'react';
    import useLocalStorage from '@/hooks/useLocalStorage.jsx';
    import { useToast } from '@/components/ui/use-toast.jsx';

    const EventContext = createContext();

    export const useEvents = () => useContext(EventContext);

    export const EventProvider = ({ children }) => {
      const [events, setEvents] = useLocalStorage('events', []);
      const { toast } = useToast();

      const addEvent = (event) => {
        const newEvent = { ...event, id: Date.now().toString(), rsvps: [] };
        setEvents((prevEvents) => [...prevEvents, newEvent]);
        toast({
          title: "Event Created!",
          description: `"${newEvent.name}" has been successfully created.`,
          variant: "success",
        });
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


      return (
        <EventContext.Provider value={{ events, addEvent, updateEvent, deleteEvent, getEventById, addRsvp }}>
          {children}
        </EventContext.Provider>
      );
    };
  