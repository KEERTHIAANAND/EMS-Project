
import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card.jsx';
import { Button, buttonVariants } from '@/components/ui/button.jsx';
import { CalendarDays, MapPin, Users, Edit, Trash2, Eye } from 'lucide-react';
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
          <CardTitle>{event.name}</CardTitle>
          <CardDescription className="flex items-center text-sm text-muted-foreground pt-1">
            <CalendarDays className="h-4 w-4 mr-2 text-primary" /> {formattedDate} at {formattedTime}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex-grow">
          <div className="flex items-center text-sm text-muted-foreground mb-3">
            <MapPin className="h-4 w-4 mr-2 text-primary" /> {event.location || 'Location TBD'}
          </div>
          <p className="text-sm text-foreground/80 line-clamp-3 mb-3">
            {event.description}
          </p>
          <div className="flex items-center text-sm text-muted-foreground">
            <Users className="h-4 w-4 mr-2 text-primary" /> {event.rsvps ? event.rsvps.length : 0} attending
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
