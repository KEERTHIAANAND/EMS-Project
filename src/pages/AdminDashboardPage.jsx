
    import React from 'react';
    import { useEvents } from '@/contexts/EventContext.jsx';
    import EventCard from '@/components/EventCard.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Link } from 'react-router-dom';
    import { motion } from 'framer-motion';
    import { PlusCircle, BarChart2, Users, Settings, Info, CalendarDays } from 'lucide-react';
    import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs.jsx";
    import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card.jsx';

    const AdminDashboardPage = () => {
      const { events } = useEvents();

      const totalEvents = events.length;
      const totalRsvps = events.reduce((sum, event) => sum + (event.rsvps ? event.rsvps.length : 0), 0);
      const upcomingEvents = events.filter(event => new Date(event.date) >= new Date()).length;


      return (
        <div className="space-y-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex flex-col sm:flex-row justify-between items-center gap-4 p-6 rounded-lg glassmorphic"
          >
            <div>
              <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
                Admin Dashboard
              </h1>
              <p className="text-muted-foreground mt-2">
                Manage events, view reports, and configure settings.
              </p>
            </div>
            <Button asChild variant="premium">
              <Link to="/create-event">
                <PlusCircle className="mr-2 h-5 w-5" /> Create New Event
              </Link>
            </Button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            <Card className="glassmorphic">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-primary">Total Events</CardTitle>
                <BarChart2 className="h-5 w-5 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-foreground">{totalEvents}</div>
                <p className="text-xs text-muted-foreground">
                  All created events
                </p>
              </CardContent>
            </Card>
            <Card className="glassmorphic">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-primary">Total RSVPs</CardTitle>
                <Users className="h-5 w-5 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-foreground">{totalRsvps}</div>
                <p className="text-xs text-muted-foreground">
                  Across all events
                </p>
              </CardContent>
            </Card>
            <Card className="glassmorphic">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-primary">Upcoming Events</CardTitle>
                <CalendarDays className="h-5 w-5 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-foreground">{upcomingEvents}</div>
                <p className="text-xs text-muted-foreground">
                  Events yet to happen
                </p>
              </CardContent>
            </Card>
          </motion.div>

          <Tabs defaultValue="manage-events" className="w-full">
            <TabsList className="grid w-full grid-cols-2 md:grid-cols-4 mb-6 glassmorphic">
              <TabsTrigger value="manage-events">Manage Events</TabsTrigger>
              <TabsTrigger value="reports" disabled>Reports (Soon)</TabsTrigger>
              <TabsTrigger value="attendees" disabled>Attendees (Soon)</TabsTrigger>
              <TabsTrigger value="settings" disabled>Settings (Soon)</TabsTrigger>
            </TabsList>
            
            <TabsContent value="manage-events">
              <h2 className="text-2xl font-semibold mb-6 text-foreground">Manage Your Events</h2>
              {events.length === 0 ? (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="text-center py-12"
                >
                  <Info className="h-16 w-16 mx-auto text-primary mb-4" />
                  <h3 className="text-xl font-semibold text-foreground mb-2">No Events to Manage</h3>
                  <p className="text-muted-foreground mb-6">
                    Create your first event to see it listed here for management.
                  </p>
                  <img  alt="Empty desk with a single plant" class="mx-auto rounded-lg shadow-xl w-full max-w-sm h-auto" src="https://images.unsplash.com/photo-1481529402569-14288964caa4" />
                </motion.div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {events.map((event, index) => (
                    <motion.div
                      key={event.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                    >
                      <EventCard event={event} isAdminView={true} />
                    </motion.div>
                  ))}
                </div>
              )}
            </TabsContent>
            <TabsContent value="reports">
              <Card className="glassmorphic">
                <CardHeader>
                  <CardTitle>Event Reports</CardTitle>
                  <CardDescription>Detailed analytics for your events (Coming Soon).</CardDescription>
                </CardHeader>
                <CardContent className="text-center py-10">
                  <BarChart2 className="h-16 w-16 mx-auto text-primary mb-4" />
                  <p className="text-muted-foreground">Ticket sales, attendance tracking, and feedback analysis will be available here.</p>
                </CardContent>
              </Card>
            </TabsContent>
             <TabsContent value="attendees">
              <Card className="glassmorphic">
                <CardHeader>
                  <CardTitle>Attendee Management</CardTitle>
                  <CardDescription>View and manage event attendees (Coming Soon).</CardDescription>
                </CardHeader>
                <CardContent className="text-center py-10">
                  <Users className="h-16 w-16 mx-auto text-primary mb-4" />
                  <p className="text-muted-foreground">A comprehensive list of attendees and their details will be shown here.</p>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="settings">
              <Card className="glassmorphic">
                <CardHeader>
                  <CardTitle>System Settings</CardTitle>
                  <CardDescription>Configure payment gateways and other system settings (Coming Soon).</CardDescription>
                </CardHeader>
                <CardContent className="text-center py-10">
                  <Settings className="h-16 w-16 mx-auto text-primary mb-4" />
                  <p className="text-muted-foreground">Options for Stripe integration and other configurations will be available.</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      );
    };

    export default AdminDashboardPage;
  