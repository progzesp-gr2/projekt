/**
 * To jest plik do routowania - przesyła użytkownika na odpowiednią stronę po URLu.
 */
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/LoginPage';
import ProjectSelectionPage from './pages/ProjectSelectionPage';
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
        <Route path="/programmer" element={<ProjectSelectionPage role="programmer"  />} />
        <Route path="/scrum-master" element={<ProjectSelectionPage role="scrum_master" />} />
        <Route path="/scrum-master/project/:id" element={<ScrumMaster />}/>
        <Route path="/programmer/project/:id" element={<Programmer />}/>
        <Route path="/product-owner" element={<ProjectSelectionPage role="product_owner"  />} /> {/*tu wybieramy projekt jaki chcemy przeglądać*/}
        <Route path="/product-owner/project/:id" element={<ProjectDashboard />}/> {/*tu już jest wybrany projekt i ładujemy konkretny layout*/}
      </Routes>
    </Router>
  );
}

export default App;
