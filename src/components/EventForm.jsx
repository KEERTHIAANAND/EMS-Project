
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
    import { CalendarPlus, Save, ArrowLeft, Loader2, CheckCircle, AlertCircle } from 'lucide-react';

    const EventForm = ({ isEditMode = false }) => {
      const { addEvent, getEventById, updateEvent, loading } = useEvents();
      const navigate = useNavigate();
      const { eventId } = useParams();
      const { toast } = useToast();

      const [eventName, setEventName] = useState('');
      const [eventDate, setEventDate] = useState(null);
      const [eventTime, setEventTime] = useState('');
      const [eventLocation, setEventLocation] = useState('');
      const [eventDescription, setEventDescription] = useState('');
      const [eventImage, setEventImage] = useState('');
      const [maxSeats, setMaxSeats] = useState(50);
      const [submitting, setSubmitting] = useState(false);
      const [message, setMessage] = useState({ type: '', text: '' });

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
            setMaxSeats(eventToEdit.max_seats || 50);
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

      const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage({ type: '', text: '' });

        // Basic validation
        if (!eventName || !eventDate || !eventTime || !eventLocation || !eventDescription) {
          setMessage({ type: 'error', text: 'Please fill in all required fields.' });
          return;
        }

        // Check authentication
        const token = localStorage.getItem('token');
        const isAuth = localStorage.getItem('isAuthenticated') === 'true';
        if (!token || !isAuth) {
          setMessage({ type: 'error', text: 'Please login to create events.' });
          return;
        }

        setSubmitting(true);

        const eventData = {
          name: eventName,
          date: eventDate ? eventDate.toISOString().split('T')[0] : '', // Store as YYYY-MM-DD
          time: eventTime,
          location: eventLocation,
          description: eventDescription,
          image: eventImage, // Store image URL
          max_seats: maxSeats,
        };

        try {
          if (isEditMode && eventId) {
            updateEvent({ ...eventData, id: eventId });
            navigate(`/events/${eventId}`);
          } else {
            // Call the async addEvent function
            const success = await addEvent(eventData);

            if (success) {
              // The success message comes from the backend response
              setMessage({ type: 'success', text: 'Event created successfully! Redirecting...' });

              // Redirect after showing success message
              setTimeout(() => {
                navigate('/');
              }, 1500);
            } else {
              setMessage({ type: 'error', text: 'Failed to create event. Please try again.' });
            }
          }
        } catch (error) {
          console.error('Error creating event:', error);
          setMessage({ type: 'error', text: 'An unexpected error occurred. Please try again.' });
        } finally {
          setSubmitting(false);
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
              {/* Message Display */}
              {message.text && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`p-4 rounded-lg mb-6 flex items-center gap-3 ${
                    message.type === 'success'
                      ? 'bg-green-500/10 border border-green-500/20 text-green-400'
                      : 'bg-red-500/10 border border-red-500/20 text-red-400'
                  }`}
                >
                  {message.type === 'success' ? (
                    <CheckCircle className="h-5 w-5 flex-shrink-0" />
                  ) : (
                    <AlertCircle className="h-5 w-5 flex-shrink-0" />
                  )}
                  <span className="text-sm">{message.text}</span>
                </motion.div>
              )}

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

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                    <Label htmlFor="maxSeats" className="text-foreground/90">Max Seats</Label>
                    <Input
                      id="maxSeats"
                      type="number"
                      min="1"
                      max="10000"
                      value={maxSeats}
                      onChange={(e) => setMaxSeats(parseInt(e.target.value) || 50)}
                      placeholder="50"
                      required
                      className="bg-background/70"
                    />
                  </div>
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

                <Button type="submit" className="w-full" variant="premium" disabled={submitting || loading}>
                  {submitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {isEditMode ? 'Saving Changes...' : 'Creating Event...'}
                    </>
                  ) : (
                    <>
                      <Save className="h-5 w-5 mr-2" />
                      {isEditMode ? 'Save Changes' : 'Create Event'}
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      );
    };

    export default EventForm;
