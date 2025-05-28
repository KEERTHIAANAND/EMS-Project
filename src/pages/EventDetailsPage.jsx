
import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useEvents } from '@/contexts/EventContext.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { CalendarDays, MapPin, Clock, Users, ArrowLeft, Edit, Trash2, Send, UserPlus } from 'lucide-react';
import { motion } from 'framer-motion';
import { useToast } from '@/components/ui/use-toast.jsx';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog.jsx";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog.jsx";

const EventDetailsPage = () => {
  const { eventId } = useParams();
  const { getEventById, deleteEvent, addRsvp } = useEvents();
  const event = getEventById(eventId);
  const navigate = useNavigate();
  const { toast } = useToast();

  const [rsvpName, setRsvpName] = useState('');
  const [rsvpEmail, setRsvpEmail] = useState('');
  const [isRsvpDialogOpen, setIsRsvpDialogOpen] = useState(false);

  if (!event) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-semibold">Event Not Found</h2>
        <p className="text-muted-foreground">The event you are looking for does not exist or may have been removed.</p>
        <Button asChild variant="link" className="mt-4">
          <Link to="/">Go to Homepage</Link>
        </Button>
      </div>
    );
  }

  const handleDelete = () => {
    deleteEvent(eventId);
    navigate('/');
  };

  const handleRsvpSubmit = (e) => {
    e.preventDefault();
    if (!rsvpName || !rsvpEmail) {
      toast({ title: "Error", description: "Please enter your name and email.", variant: "destructive" });
      return;
    }
    addRsvp(eventId, { name: rsvpName, email: rsvpEmail });
    setRsvpName('');
    setRsvpEmail('');
    setIsRsvpDialogOpen(false);
  };

  const formattedDate = event.date ? new Date(event.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : 'Date TBD';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="overflow-hidden glassmorphic">
        <CardHeader className="relative">
          {event.image ? (
            <img src={event.image} alt={event.name} className="w-full h-64 object-cover rounded-t-lg" />
          ) : (
            <div className="w-full h-64 bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center rounded-t-lg">
              <CalendarDays className="h-24 w-24 text-white/70" />
            </div>
          )}
          <div className="absolute top-4 left-4">
            <Button variant="outline" size="icon" onClick={() => navigate(-1)} className="bg-background/70 hover:bg-background/90">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </div>
          <div className="absolute top-4 right-4 flex space-x-2">
            <Button variant="outline" size="icon" onClick={() => navigate(`/admin/edit-event/${eventId}`)} className="bg-background/70 hover:bg-background/90">
              <Edit className="h-5 w-5 text-blue-400" />
            </Button>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="outline" size="icon" className="bg-background/70 hover:bg-background/90">
                  <Trash2 className="h-5 w-5 text-red-400" />
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete the event "{event.name}".
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleDelete} className="bg-destructive hover:bg-destructive/90 text-destructive-foreground">
                    Delete
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </CardHeader>
        <CardContent className="p-6 space-y-6">
          <CardTitle className="text-4xl mb-2">{event.name}</CardTitle>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-lg">
            <div className="flex items-center text-muted-foreground">
              <CalendarDays className="h-6 w-6 mr-3 text-primary" />
              <span>{formattedDate}</span>
            </div>
            <div className="flex items-center text-muted-foreground">
              <Clock className="h-6 w-6 mr-3 text-primary" />
              <span>{event.time || 'Time TBD'}</span>
            </div>
            <div className="flex items-center text-muted-foreground md:col-span-2">
              <MapPin className="h-6 w-6 mr-3 text-primary" />
              <span>{event.location || 'Location TBD'}</span>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-semibold text-foreground mb-2">About this event</h3>
            <p className="text-foreground/80 whitespace-pre-wrap leading-relaxed">
              {event.description}
            </p>
          </div>

          <div className="border-t border-border pt-6">
            <h3 className="text-xl font-semibold text-foreground mb-3 flex items-center">
              <Users className="h-6 w-6 mr-3 text-primary" />
              Attendees ({event.rsvps ? event.rsvps.length : 0})
            </h3>
            {event.rsvps && event.rsvps.length > 0 ? (
              <ul className="space-y-2">
                {event.rsvps.map(rsvp => (
                  <li key={rsvp.id} className="text-sm text-muted-foreground p-2 bg-foreground/5 rounded-md">{rsvp.name} ({rsvp.email})</li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted-foreground">No attendees have RSVP'd yet.</p>
            )}
          </div>

        </CardContent>
        <CardFooter className="p-6 bg-background/30">
          <Dialog open={isRsvpDialogOpen} onOpenChange={setIsRsvpDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="premium" size="lg" className="w-full sm:w-auto">
                <UserPlus className="mr-2 h-5 w-5" /> RSVP for this Event
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>RSVP for {event.name}</DialogTitle>
                <DialogDescription>
                  Enter your details to confirm your attendance.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleRsvpSubmit} className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="rsvp-name" className="text-right">
                    Name
                  </Label>
                  <Input id="rsvp-name" value={rsvpName} onChange={(e) => setRsvpName(e.target.value)} className="col-span-3" placeholder="Your Name" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="rsvp-email" className="text-right">
                    Email
                  </Label>
                  <Input id="rsvp-email" type="email" value={rsvpEmail} onChange={(e) => setRsvpEmail(e.target.value)} className="col-span-3" placeholder="your@email.com" />
                </div>
                <DialogFooter>
                  <DialogClose asChild>
                    <Button type="button" variant="outline">Cancel</Button>
                  </DialogClose>
                  <Button type="submit">
                    <Send className="mr-2 h-4 w-4" /> Confirm RSVP
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </CardFooter>
      </Card>
    </motion.div>
  );
};

export default EventDetailsPage;
