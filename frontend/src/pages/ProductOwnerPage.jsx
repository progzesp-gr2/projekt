/**
 * Tutaj pojawia się product owner zaraz po zalogowaniu
 To jest strona wyboru projektu, każdy product owner może mieć ich kilka 
 Na tej stronie product owner wybiera:
 - projekt jaki chce przejrzeć
 - tworzy projekty 
 - dodaje ludzi do projektów
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';



export default function ProductOwnerPage() {

  const navigate = useNavigate();
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');

  //dla testów
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
  ]);

  //Dodawanie projektu
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

  //usuwanie projektu
  const handleDeleteProject = (projectId) => {

    if (!window.confirm('Usunąć projekt?')) return;

    setProjects((prev) =>
      prev.filter((project) => project.id !== projectId)
    );
  };

  //dodawanie programistów
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
    <div className="p-8">

      <h1 className="text-3xl font-bold mb-8">
        Your Projects
      </h1>

      <div className="space-y-4">

        {projects.map((project) => (
          <div
            key={project.id}
            onClick={() =>
              navigate(`/product-owner/project/${project.id}`)
            }
            className="p-6 rounded-xl border cursor-pointer hover:scale-[1.01] transition-all"
          >
            <h2 className="text-xl font-bold">
              {project.name}
            </h2>
          </div>
        ))}

      </div>
    </div>
  );
}