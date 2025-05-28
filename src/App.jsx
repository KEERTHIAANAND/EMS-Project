import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '@/components/Layout.jsx';
import HomePage from '@/pages/HomePage.jsx';
import CreateEventPage from '@/pages/CreateEventPage.jsx';
import EditEventPage from '@/pages/EditEventPage.jsx';
import EventDetailsPage from '@/pages/EventDetailsPage.jsx';
import AdminDashboardPage from '@/pages/AdminDashboardPage.jsx';
import NotFoundPage from '@/pages/NotFoundPage.jsx';
import SignInPage from '@/pages/SignInPage.jsx';
import { EventProvider } from '@/contexts/EventContext.jsx';

function App() {
  // Simple auth check - replace with your actual auth logic
  const isAuthenticated = () => {
    return localStorage.getItem('isAuthenticated') === 'true';
  };

  // Protected route component
  const ProtectedRoute = ({ children }) => {
    if (!isAuthenticated()) {
      return <Navigate to="/sign-in" />;
    }
    return children;
  };

  return (
    <EventProvider>
      <Router>
        <Routes>
          <Route path="/sign-in" element={<SignInPage />} />
          
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
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