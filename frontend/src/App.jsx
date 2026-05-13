/**
 * To jest plik do routowania.
 * Bardzo ważne jest to że kiedy będzie tworzony endpoint
 * do przeglądania projektów przed product ownera to ważne żeby wyglądał on tak:
 * "/product-owner/project/:id"
 */
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/LoginPage';
import ProductOwner from './pages/ProductOwnerPage';
import ProjectDashboard from './pages/ProjectDashboardPage';
import Register from './pages/RegisterPage';
import Dashboard from './pages/DashboardPage';
import Programmer from './pages/ProgrammerPage';
import ScrumMaster from './pages/ScrumMasterPage';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register" element={<Register />} />
        <Route path="/programmer" element={<Programmer />} />
        <Route path="/scrum-master" element={<ScrumMaster />} />
        <Route path="/product-owner" element={<ProductOwner />} /> //tu wybieramy projekt jaki chcemy przeglądać
        <Route path="/product-owner/project/:id" element={<ProjectDashboard />}/> //tu już jest wybrany projekt i ładujemy konkretny layout
      </Routes>
    </Router>
  );
}

export default App;