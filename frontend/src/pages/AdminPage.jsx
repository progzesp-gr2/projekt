import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AdminPage() {
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState('users');

  const stats = [
    { label: 'Liczba użytkowników', value: '1', color: '#aa3bff' },
    { label: 'Projekty', value: '3', color: '#3b82f6' },
    { label: 'Wszystkie zadania', value: '1', color: '#10b981' },
    { label: 'Ukończone', value: '0', percentage: '0%', color: '#10b981' },
  ];

  const [users, setUsers] = useState([
    { id: 'AA', name: 'Admin Admin', email: 'admin@admin.pl', role: 'Administrator', tasks: 1 },
  ]);

  // tymczasowi programiści w do testów
  const [programmers] = useState([
    { id: 'P1', name: 'Jan Kowalski', email: 'jan@test.pl', role: 'Programmer' },
    { id: 'P2', name: 'Anna Nowak', email: 'anna@test.pl', role: 'Programmer' },
    { id: 'P3', name: 'Piotr Zielinski', email: 'piotr@test.pl', role: 'Programmer' },
  ]);

  const [projects, setProjects] = useState([
    {
      id: 1,
      name: 'ScrumBoard App',
      description: 'Aplikacja do zarządzania projektami scrumowymi',
      members: [],
    },
  ]);

  const [selectedProjectId, setSelectedProjectId] = useState(1);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');

  const selectedProject = projects.find(
    (project) => project.id === selectedProjectId
  );

  const handleCreateProject = (e) => {
    e.preventDefault();

    if (newProjectName.trim() === "") return;

    const newProject = {
      id: Date.now(),
      name: newProjectName,
      description: newProjectDescription,
      members: [],
    };

    setProjects([...projects, newProject]);
    setSelectedProjectId(newProject.id);
    setNewProjectName('');
    setNewProjectDescription('');
  };

  const handleAddProgrammer = (programmer, projectId) => {
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
    <div className="flex-1 flex flex-col p-8 text-left bg-gray-50/30">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h2 className="m-0 text-2xl font-bold" style={{ color: 'var(--text-h)' }}>Panel Administracyjny</h2>
          <p className="text-sm opacity-60">Zarządzanie systemem Scrum</p>
        </div>
        <button 
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-md border text-sm font-medium hover:bg-gray-100 transition-all"
          style={{ borderColor: 'var(--border)', backgroundColor: 'var(--bg)' }}
        >
          Wyloguj
        </button>
      </header>

      {/* statystyki */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        {stats.map((stat, i) => (
          <div 
            key={i} 
            className="p-6 rounded-xl border flex justify-between items-start"
            style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)', boxShadow: 'var(--shadow)' }}
          >
            <div>
              <p className="text-xs font-semibold uppercase opacity-50 mb-1">{stat.label}</p>
              <h1 className="m-0 text-3xl font-black">{stat.value}</h1>
            </div>
            <span className="text-sm font-bold text-green-500">{stat.percentage}</span>
          </div>
        ))}
      </div>

      {/* nawigacja zakładek */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex gap-2 p-1 rounded-lg bg-gray-100 border" style={{ borderColor: 'var(--border)' }}>
          {['users', 'projects', 'settings'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all ${
                activeTab === tab ? 'bg-white shadow-sm opacity-100' : 'opacity-60 hover:opacity-100'
              }`}
            >
              {tab === 'users' && 'Użytkownicy'}
              {tab === 'projects' && 'Projekty'}
              {tab === 'settings' && 'Ustawienia'}
            </button>
          ))}
        </div>
      </div>

      {/* content zakładki*/}
      <div 
        className="rounded-xl border overflow-hidden min-h-[300px] flex flex-col" 
        style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)', boxShadow: 'var(--shadow)' }}
      >
        {activeTab === 'users' ? (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b" style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}>
                <th className="p-4 text-xs uppercase opacity-60">Użytkownik</th>
                <th className="p-4 text-xs uppercase opacity-60">Email</th>
                <th className="p-4 text-xs uppercase opacity-60">Rola</th>
                <th className="p-4 text-xs uppercase opacity-60">Liczba zadań</th>
                <th className="p-4 text-xs uppercase opacity-60 text-right">Akcje</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, idx) => (
                <tr key={idx} className="border-b last:border-0 hover:bg-gray-50/50 transition-colors" style={{ borderColor: 'var(--border)' }}>
                  <td className="p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-xs" style={{ backgroundColor: 'var(--accent)' }}>
                      {user.id}
                    </div>
                    <span className="font-medium" style={{ color: 'var(--text-h)' }}>{user.name}</span>
                  </td>
                  <td className="p-4 text-sm opacity-80">{user.email}</td>
                  <td className="p-4">
                    <span className="px-3 py-1 rounded-full text-[10px] font-bold bg-gray-100 border">
                      {user.role}
                    </span>
                  </td>
                  <td className="p-4 text-sm font-medium">{user.tasks}</td>
                  <td className="p-4 text-right">
                    <button className="mr-3 opacity-40 hover:opacity-100">Edytuj</button>
                    <button className="opacity-40 hover:opacity-100 text-red-500">Usuń</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
                  ) : activeTab === 'projects' ? (
            <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">

              {/* Lista projektów */}
              <div className="lg:col-span-1">
                <h3 className="font-bold mb-4" style={{ color: 'var(--text-h)' }}>
                  Aktualne projekty
                </h3>

                <div className="space-y-3">
                  {projects.map((project) => (
                    <button
                      key={project.id}
                      onClick={() => setSelectedProjectId(project.id)}
                      className={`w-full text-left p-4 rounded-lg border transition-all ${
                        selectedProjectId === project.id ? 'ring-2' : ''
                      }`}
                      style={{
                        backgroundColor: 'var(--code-bg)',
                        borderColor: 'var(--border)',
                        ringColor: 'var(--accent)',
                      }}
                    >
                      <p className="font-bold">{project.name}</p>
                      <p className="text-sm opacity-60">
                        Członkowie: {project.members.length}
                      </p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Szczegóły projektu */}
              <div className="lg:col-span-1">
                <h3 className="font-bold mb-4" style={{ color: 'var(--text-h)' }}>
                  Szczegóły projektu
                </h3>

                {selectedProject && (
                  <div
                    className="p-5 rounded-lg border"
                    style={{
                      backgroundColor: 'var(--code-bg)',
                      borderColor: 'var(--border)',
                    }}
                  >
                    <h2 className="text-xl font-bold mb-2">{selectedProject.name}</h2>
                    <p className="text-sm opacity-70 mb-6">
                      {selectedProject.description || 'Brak opisu projektu'}
                    </p>

                    <h4 className="font-bold mb-3">Programiści w projekcie</h4>

                    {selectedProject.members.length === 0 ? (
                      <p className="text-sm opacity-60">
                        Brak dodanych programistów.
                      </p>
                    ) : (
                      <div className="space-y-2">
                        {selectedProject.members.map((member) => (
                          <div
                            key={member.id}
                            className="p-3 rounded border text-sm"
                            style={{ borderColor: 'var(--border)' }}
                          >
                            <p className="font-bold">{member.name}</p>
                            <p className="opacity-60">{member.email}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Tworzenie projektu + dodawanie ludzi */}
              <div className="lg:col-span-1 space-y-6">

                <form
                  onSubmit={handleCreateProject}
                  className="p-5 rounded-lg border"
                  style={{
                    backgroundColor: 'var(--code-bg)',
                    borderColor: 'var(--border)',
                  }}
                >
                  <h3 className="font-bold mb-4">Utwórz nowy projekt</h3>

                  <input
                    type="text"
                    value={newProjectName}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    placeholder="Nazwa projektu"
                    className="w-full px-4 py-2 mb-3 rounded border"
                    style={{
                      backgroundColor: 'var(--bg)',
                      borderColor: 'var(--border)',
                    }}
                  />

                  <textarea
                    value={newProjectDescription}
                    onChange={(e) => setNewProjectDescription(e.target.value)}
                    placeholder="Opis projektu"
                    className="w-full px-4 py-2 mb-3 rounded border resize-none"
                    rows="3"
                    style={{
                      backgroundColor: 'var(--bg)',
                      borderColor: 'var(--border)',
                    }}
                  />

                  <button
                    type="submit"
                    className="w-full py-2 rounded-lg font-bold text-white"
                    style={{ backgroundColor: 'var(--accent)' }}
                  >
                    Dodaj projekt
                  </button>
                </form>

                <div
                  className="p-5 rounded-lg border"
                  style={{
                    backgroundColor: 'var(--code-bg)',
                    borderColor: 'var(--border)',
                  }}
                >
                  <h3 className="font-bold mb-4">Dodaj programistę</h3>

                  <div className="space-y-3">
                    {programmers.map((programmer) => { //żeby nie dodawać 2 razy tego samego gościa
                      const alreadyAdded = selectedProject?.members.some(
                        (member) => member.id === programmer.id
                      ) || false;

                      return (
                        <div
                          key={programmer.id}
                          className="p-3 rounded border flex justify-between items-center"
                          style={{ borderColor: 'var(--border)' }}
                        >
                          <div>
                            <p className="font-bold text-sm">{programmer.name}</p>
                            <p className="text-xs opacity-60">{programmer.email}</p>
                          </div>

                          <button
                            onClick={() => handleAddProgrammer(programmer, selectedProject.id)}
                            disabled={alreadyAdded}
                            className="px-3 py-1 rounded text-xs font-bold text-white disabled:opacity-40"
                            style={{ backgroundColor: 'var(--accent)' }}
                          >
                            {alreadyAdded ? 'Dodany' : 'Dodaj'}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-20 text-center">
              <h2 className="mb-2">Wkrótce</h2>
            </div>
          )}

        {/* tutaj koniec */}
      </div>
    </div>
  );
}