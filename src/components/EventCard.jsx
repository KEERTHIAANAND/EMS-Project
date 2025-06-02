
import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card.jsx';
import { Button, buttonVariants } from '@/components/ui/button.jsx';
import { CalendarDays, MapPin, Users, Edit, Trash2, Eye, CheckCircle, Clock, UserX } from 'lucide-react';
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
import { useEvents } from '@/contexts/EventContext.jsx';
import { cn } from '@/lib/utils.jsx';

const EventCard = ({ event, isAdminView = false }) => {
  const { deleteEvent } = useEvents();
  const formattedDate = event.date ? new Date(event.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : 'Date TBD';
  const formattedTime = event.time || 'Time TBD';

  // Calculate event status and seats
  const isCompleted = event.is_completed || (event.date && new Date(event.date) < new Date());
  const maxSeats = event.max_seats || 50;
  const rsvpCount = event.rsvp_count || (event.rsvps ? event.rsvps.length : 0);
  const availableSeats = event.available_seats !== undefined ? event.available_seats : Math.max(0, maxSeats - rsvpCount);
  const isFull = availableSeats === 0;

  // Get status info
  const getStatusInfo = () => {
    if (isCompleted) {
      return {
        text: 'Completed',
        icon: CheckCircle,
        className: 'text-green-500 bg-green-500/10 border-green-500/20'
      };
    } else if (isFull) {
      return {
        text: 'Full',
        icon: UserX,
        className: 'text-red-500 bg-red-500/10 border-red-500/20'
      };
    } else {
      return {
        text: 'Open',
        icon: Clock,
        className: 'text-blue-500 bg-blue-500/10 border-blue-500/20'
      };
    }
  };

  const statusInfo = getStatusInfo();
  const StatusIcon = statusInfo.icon;

  const handleDelete = () => {
    deleteEvent(event.id);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.03, boxShadow: "0px 10px 20px rgba(128, 90, 213, 0.3)" }}
    >
      <Card className="overflow-hidden h-full flex flex-col">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle>{event.name}</CardTitle>
              <CardDescription className="flex items-center text-sm text-muted-foreground pt-1">
                <CalendarDays className="h-4 w-4 mr-2 text-primary" /> {formattedDate} at {formattedTime}
              </CardDescription>
            </div>
            <div className={`flex items-center gap-1 px-2 py-1 rounded-full border text-xs font-medium ${statusInfo.className}`}>
              <StatusIcon className="h-3 w-3" />
              {statusInfo.text}
            </div>
          </div>
        </CardHeader>
        <CardContent className="flex-grow">
          <div className="flex items-center text-sm text-muted-foreground mb-3">
            <MapPin className="h-4 w-4 mr-2 text-primary" /> {event.location || 'Location TBD'}
          </div>
          <p className="text-sm text-foreground/80 line-clamp-3 mb-3">
            {event.description}
          </p>
          <div className="space-y-2">
            <div className="flex items-center text-sm text-muted-foreground">
              <Users className="h-4 w-4 mr-2 text-primary" /> {rsvpCount} / {maxSeats} attending
            </div>
            <div className="flex items-center text-sm">
              {availableSeats > 0 ? (
                <span className="text-green-500 font-medium">
                  {availableSeats} seats available
                </span>
              ) : (
                <span className="text-red-500 font-medium">
                  No seats available
                </span>
              )}
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between items-center">
          <Button asChild variant="outline" size="sm">
            <Link to={`/events/${event.id}`}>
              <Eye className="h-4 w-4 mr-2" /> View Details
            </Link>
          </Button>
          {isAdminView && (
            <div className="flex space-x-2">
              <Button asChild variant="ghost" size="sm" className="text-blue-400 hover:text-blue-300">
                <Link to={`/admin/edit-event/${event.id}`}>
                  <Edit className="h-4 w-4 mr-1" /> Edit
                </Link>
              </Button>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="ghost" size="sm" className="text-red-400 hover:text-red-300">
                    <Trash2 className="h-4 w-4 mr-1" /> Delete
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
                    <AlertDialogAction onClick={handleDelete} className={cn(buttonVariants({ variant: "destructive" }))}>
                      Delete
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          )}
        </CardFooter>
      </Card>
    </motion.div>
  );
};

export default EventCard;
