
    import React from 'react';
    import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
    import Layout from '@/components/Layout.jsx';
    import HomePage from '@/pages/HomePage.jsx';
    import CreateEventPage from '@/pages/CreateEventPage.jsx';
    import EditEventPage from '@/pages/EditEventPage.jsx';
    import EventDetailsPage from '@/pages/EventDetailsPage.jsx';
    import AdminDashboardPage from '@/pages/AdminDashboardPage.jsx';
    import NotFoundPage from '@/pages/NotFoundPage.jsx';
    import { EventProvider } from '@/contexts/EventContext.jsx';

    function App() {
      return (
        <EventProvider>
          <Router>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<HomePage />} />
                <Route path="create-event" element={<CreateEventPage />} />
                <Route path="events/:eventId" element={<EventDetailsPage />} />
                <Route path="admin" element={<AdminDashboardPage />} />
                <Route path="admin/edit-event/:eventId" element={<EditEventPage />} />
                <Route path="*" element={<NotFoundPage />} />
              </Route>
            </Routes>
          </Router>
        </EventProvider>
      );
    }

    export default App;
  