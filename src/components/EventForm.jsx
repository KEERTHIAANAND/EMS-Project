
    import React, { useState, useEffect } from 'react';
    import { useNavigate, useParams } from 'react-router-dom';
    import { motion } from 'framer-motion';
    import { useEvents } from '@/contexts/EventContext.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Input } from '@/components/ui/input.jsx';
    import { Label } from '@/components/ui/label.jsx';
    import { Textarea } from '@/components/ui/textarea.jsx';
    import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card.jsx';
    import { DatePicker } from '@/components/DatePicker.jsx';
    import { useToast } from '@/components/ui/use-toast.jsx';
    import { CalendarPlus, Save, ArrowLeft } from 'lucide-react';

    const EventForm = ({ isEditMode = false }) => {
      const { addEvent, getEventById, updateEvent } = useEvents();
      const navigate = useNavigate();
      const { eventId } = useParams();
      const { toast } = useToast();

      const [eventName, setEventName] = useState('');
      const [eventDate, setEventDate] = useState(null);
      const [eventTime, setEventTime] = useState('');
      const [eventLocation, setEventLocation] = useState('');
      const [eventDescription, setEventDescription] = useState('');
      const [eventImage, setEventImage] = useState('');

      useEffect(() => {
        if (isEditMode && eventId) {
          const eventToEdit = getEventById(eventId);
          if (eventToEdit) {
            setEventName(eventToEdit.name);
            setEventDate(eventToEdit.date ? new Date(eventToEdit.date) : null);
            setEventTime(eventToEdit.time);
            setEventLocation(eventToEdit.location);
            setEventDescription(eventToEdit.description);
            setEventImage(eventToEdit.image || '');
          } else {
            toast({
              title: "Error",
              description: "Event not found.",
              variant: "destructive",
            });
            navigate('/admin'); 
          }
        }
      }, [isEditMode, eventId, getEventById, navigate, toast]);

      const handleSubmit = (e) => {
        e.preventDefault();
        if (!eventName || !eventDate || !eventTime || !eventLocation || !eventDescription) {
          toast({
            title: "Missing Information",
            description: "Please fill in all required fields.",
            variant: "destructive",
          });
          return;
        }

        const eventData = {
          name: eventName,
          date: eventDate ? eventDate.toISOString().split('T')[0] : '', // Store as YYYY-MM-DD
          time: eventTime,
          location: eventLocation,
          description: eventDescription,
          image: eventImage, // Store image URL
        };

        if (isEditMode && eventId) {
          updateEvent({ ...eventData, id: eventId });
          navigate(`/events/${eventId}`);
        } else {
          addEvent(eventData);
          navigate('/');
        }
      };

      return (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="max-w-2xl mx-auto glassmorphic">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center">
                  <CalendarPlus className="h-7 w-7 mr-3 text-primary" />
                  {isEditMode ? 'Edit Event' : 'Create New Event'}
                </CardTitle>
                <Button variant="outline" size="sm" onClick={() => navigate(isEditMode ? `/events/${eventId}` : '/')}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back
                </Button>
              </div>
              <CardDescription>
                {isEditMode ? 'Update the details of your event.' : 'Fill in the details to create a new exciting event.'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="eventName" className="text-foreground/90">Event Name</Label>
                  <Input
                    id="eventName"
                    value={eventName}
                    onChange={(e) => setEventName(e.target.value)}
                    placeholder="e.g., Summer Music Festival"
                    required
                    className="bg-background/70"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="eventDate" className="text-foreground/90">Date</Label>
                    <DatePicker date={eventDate} setDate={setEventDate} className="bg-background/70 w-full" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="eventTime" className="text-foreground/90">Time</Label>
                    <Input
                      id="eventTime"
                      type="time"
                      value={eventTime}
                      onChange={(e) => setEventTime(e.target.value)}
                      required
                      className="bg-background/70"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="eventLocation" className="text-foreground/90">Location</Label>
                  <Input
                    id="eventLocation"
                    value={eventLocation}
                    onChange={(e) => setEventLocation(e.target.value)}
                    placeholder="e.g., Central Park, New York"
                    required
                    className="bg-background/70"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="eventImage" className="text-foreground/90">Image URL (Optional)</Label>
                  <Input
                    id="eventImage"
                    value={eventImage}
                    onChange={(e) => setEventImage(e.target.value)}
                    placeholder="e.g., https://example.com/event-image.jpg"
                    className="bg-background/70"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="eventDescription" className="text-foreground/90">Description</Label>
                  <Textarea
                    id="eventDescription"
                    value={eventDescription}
                    onChange={(e) => setEventDescription(e.target.value)}
                    placeholder="Describe your event..."
                    rows={4}
                    required
                    className="bg-background/70"
                  />
                </div>

                <Button type="submit" className="w-full" variant="premium">
                  <Save className="h-5 w-5 mr-2" />
                  {isEditMode ? 'Save Changes' : 'Create Event'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      );
    };

    export default EventForm;
  