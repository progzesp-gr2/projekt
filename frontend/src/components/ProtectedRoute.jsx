import { Navigate } from 'react-router-dom';


// fsprawdza czy jest token 
// potrzebne na samym początku przed loginem
export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access');

  
  if (!token) {
    return <Navigate to="/login" />;
  }

  
  return children;  // childrew to bedzie Dashboard
}