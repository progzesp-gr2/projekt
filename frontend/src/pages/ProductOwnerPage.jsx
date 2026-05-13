/**
 * Tutaj pojawia się product owner zaraz po zalogowaniu
 * To jest strona wyboru projektu, każdy product owner może mieć ich kilka
 *
 * Na tej stronie product owner:
 * - wybiera projekt jaki chce przejrzeć
 * - tworzy projekty
 * - dodaje ludzi do projektów
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ProjectManagementPanel from '../components/ProjectManagementPanel';

export default function ProductOwnerPage() {

  const navigate = useNavigate();
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');

   //domyslnie nie pokazuję menu dodawania projektów
  const [showProjectPanel, setShowProjectPanel] = useState(false);

  // Tymczasowe projekty do testów
  const [projects, setProjects] = useState([
    {
      id: 1,
      name: 'ScrumBoard App',
      description: 'Aplikacja scrumowa',
      members: [],
    },
    {
      id: 2,
      name: 'Airport System',
      description: 'System lotniskowy',
      members: [],
    },
  ]);

  
  const [programmers] = useState([
    {
      id: 'P1',
      name: 'Jan Kowalski',
      email: 'jan@example.com',
    },
    {
      id: 'P2',
      name: 'Anna Nowak',
      email: 'anna@example.com',
    },
    {
      id: 'P3',
      name: 'Piotr Zielinski',
      email: 'piotr@example.com',
    },
  ]);

 
  const [selectedProjectId, setSelectedProjectId] = useState(1);
  const selectedProject = projects.find(
    (project) => project.id === selectedProjectId
  );


  const handleCreateProject = (e) => {

    e.preventDefault();

    if (newProjectName.trim() === '') return;

    const newProject = {
      id: Date.now(),
      name: newProjectName,
      description: newProjectDescription,
      members: [],
    };

    setProjects((prev) => [...prev, newProject]);

    setNewProjectName('');
    setNewProjectDescription('');
  };

  
  const handleDeleteProject = (projectId) => {

    if (!window.confirm('Usunąć projekt?')) return;

    setProjects((prev) =>
      prev.filter((project) => project.id !== projectId)
    );

    if (selectedProjectId === projectId) {
      setSelectedProjectId(null);
    }
  };

  
  const handleAddProgrammer = (projectId, programmer) => {

    setProjects((prevProjects) =>
      prevProjects.map((project) => {

        if (project.id !== projectId) return project;

        const alreadyAdded = project.members.some(
          (member) => member.id === programmer.id
        );

        if (alreadyAdded) return project;

        return {
          ...project,
          members: [...project.members, programmer],
        };
      })
    );
  };

  return (
    //<div className="p-8 bg-gray-50/30 min-h-screen">
    <div
      className="p-8 min-h-screen"
      style={{ backgroundColor: 'var(--code-bg)' }}
    >

      {/* HEADER */}
      <header className="flex justify-between items-center mb-10">

        <div>
          <h1
            className="text-3xl font-bold"
            style={{ color: 'var(--text-h)' }}
          >
            Twoje projekty
          </h1>

          <p className="text-sm opacity-60">
            Zarządzanie projektami Scrum
          </p>
        </div>

        <button
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-md border text-sm font-medium hover:bg-gray-100 transition-all cursor-pointer"
          style={{
            borderColor: 'var(--border)',
            backgroundColor: 'var(--bg)',
          }}
        >
          Wyloguj
        </button>

      </header>

      <div className="flex justify-end mb-6">
        <button
          onClick={() =>
            setShowProjectPanel((prev) => !prev)
          }
          className="px-4 py-2 rounded-lg font-bold text-white cursor-pointer"
          style={{
            backgroundColor: 'var(--accent)',
          }}
        >
          {showProjectPanel
            ? 'Zamknij panel'
            : '+ Dodaj projekt'}
        </button>

      </div>

      <div className={`grid gap-6 ${
          showProjectPanel
            ? 'grid-cols-1 lg:grid-cols-3'
            : 'grid-cols-1'
        }`}>
        <div className={
          showProjectPanel
            ? 'lg:col-span-2'
            : ''
        }>
          <div className="space-y-4">

            {projects.map((project) => {

              const isSelected =
                selectedProjectId === project.id;

              return (
                <div
                  key={project.id}
                  onClick={() =>
                    setSelectedProjectId(project.id)
                  }
                  className={`p-6 rounded-xl border transition-all cursor-pointer ${
                    isSelected ? 'ring-2' : ''
                  }`}
                  style={{
                    backgroundColor: 'var(--bg)',
                    borderColor: 'var(--border)',
                    boxShadow: 'var(--shadow)',
                    ringColor: 'var(--accent)',
                  }}
                >

                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-xl font-bold mb-1">
                        {project.name}
                      </h2>

                      <p className="text-sm opacity-70 mb-3">
                        {project.description}
                      </p>

                      <p className="text-sm opacity-60">
                        Członkowie projektu:{' '}
                        {project.members.length}
                      </p>

                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();

                          navigate(
                            `/product-owner/project/${project.id}`
                          );
                        }}
                        className="px-4 py-2 rounded-md text-sm font-bold text-white cursor-pointer"
                        style={{
                          backgroundColor: 'var(--accent)',
                        }}
                      >
                        Open
                      </button>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();

                          handleDeleteProject(project.id);
                        }}
                        className="px-4 py-2 rounded-md border text-sm font-bold text-red-500 hover:bg-red-50 transition-all cursor-pointer"
                        style={{
                          borderColor: 'var(--border)',
                          backgroundColor: 'var(--bg)',
                        }}
                      >
                        Usuń
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {showProjectPanel && (
          <ProjectManagementPanel
            programmers={programmers}
            selectedProject={selectedProject}

            newProjectName={newProjectName}
            setNewProjectName={setNewProjectName}

            newProjectDescription={newProjectDescription}
            setNewProjectDescription={setNewProjectDescription}

            handleCreateProject={handleCreateProject}
            handleAddProgrammer={handleAddProgrammer}
          />
        )}

      </div>

    </div>
  );
}