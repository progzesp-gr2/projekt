import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ScrumMasterPage() {
  const navigate = useNavigate();

  const [selectedSprintId, setSelectedSprintId] = useState(1);

  const [tasks, setTasks] = useState([
    { id: 1, sprintId: 1, title: 'Stworzyć ekran logowania', assignedTo: ['Jan Kowalski'], status: 'W trakcie', priority: 'Neutralny', type: 'Feature'},
  ]);

  const [newTask, setNewTask] = useState('');

  // robocza lista osób, po połączeniu z backendem do wyrzucenia
  const [teamMembers] = useState([
    { id: 'P1', name: 'Jan Kowalski' },
    { id: 'P2', name: 'Anna Nowak' },
    { id: 'P3', name: 'Piotr Zielinski' },
  ]);

  const [editingTaskId, setEditingTaskId] = useState(null);

  // też roboczo
  const [sprints, setSprints] = useState([
    { id: 1, name: 'Sprint 1', status: 'Aktywny', startDate: '14.05.2026', endDate: '21.05.2026' }
  ]);
  const [isAddSprintModalOpen, setIsAddSprintModalOpen] = useState(false);
  const [newSprintName, setNewSprintName] = useState('');
  const [newSprintStatus, setNewSprintStatus] = useState('Planowany');
  const [editingSprintId, setEditingSprintId] = useState(null);
  const [newSprintStartDate, setNewSprintStartDate] = useState('');
  const [newSprintEndDate, setNewSprintEndDate] = useState('');

  const handleAddTask = (e) => {
    e.preventDefault();

    if (!newTask.trim() || !selectedSprintId) return;

    setTasks([
      ...tasks,
      {
        id: Date.now(),
        sprintId: selectedSprintId,
        title: newTask,
        assignedTo: [],
        status: 'Do zrobienia',
        priority: 'Neutralny',
        type: 'Feature'
      },
    ]);

    setNewTask('');
  };

  const handleAddSprint = (e) => {
    e.preventDefault();

    if (!newSprintName.trim()) return;

    setSprints([
      ...sprints,
      {
        id: Date.now(),
        name: newSprintName.trim(),
        status: newSprintStatus,
        startDate: newSprintStartDate,
        endDate: newSprintEndDate,
      }
    ]);

    setNewSprintName('');
    setNewSprintStatus('Planowany');
    setNewSprintStartDate('');
    setNewSprintEndDate('');
    setIsAddSprintModalOpen(false);
  };

  const handleDeleteTask = (taskId) => {
    if (!window.confirm("Czy na pewno chcesz usunąć to zadanie?")) return;
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
  };

  const handleDeleteSprint = (e, sprintId) => {
    e.stopPropagation();
    
    if (!window.confirm("Czy na pewno chcesz usunąć ten sprint?")) return;
    
    setSprints((prevSprints) => prevSprints.filter((s) => s.id !== sprintId));
    setTasks((prevTasks) => prevTasks.filter((t) => t.sprintId !== sprintId));
    if (selectedSprintId === sprintId) {
      setSelectedSprintId(null);
    }
  };

  const handleChangeSprintStatus = (sprintId, newStatus) => {
    setSprints((prevSprints) =>
      prevSprints.map((sprint) => (sprint.id === sprintId ? { ...sprint, status: newStatus } : sprint))
    );
  };

  const handleToggleAssignee = (taskId, memberName) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => {
        if (task.id !== taskId) return task;
        const isAssigned = task.assignedTo.includes(memberName);
        const updatedAssignees = isAssigned
          ? task.assignedTo.filter((name) => name !== memberName)
          : [...task.assignedTo, memberName];

        return { ...task, assignedTo: updatedAssignees };
      })
    );
  };

  const handleChangeTaskStatus = (taskId, newStatus) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => (task.id === taskId ? { ...task, status: newStatus } : task))
    );
  };

  const handleChangeTaskPriority = (taskId, newPriority) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => (task.id === taskId ? { ...task, priority: newPriority } : task))
    );
  };

  const handleChangeTaskType = (taskId, newType) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => (task.id === taskId ? { ...task, type: newType } : task))
    );
  };

  const handleChangeSprintDate = (sprintId, field, newDate) => {
    setSprints((prevSprints) =>
      prevSprints.map((sprint) => (sprint.id === sprintId ? { ...sprint, [field]: newDate } : sprint))
    );
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'W trakcie': return 'text-yellow-500';
      case 'Ukończone': return 'text-green-500';
      case 'Do zrobienia': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Krytyczny': return 'text-red-500';
      case 'Pilny': return 'text-orange-500';
      case 'Ważny': return 'text-purple-500';
      case 'Neutralny': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'Bug': return 'text-red-500';
      case 'Feature': return 'text-blue-500';
      case 'Documentation': return 'text-green-500';
      case 'Question': return 'text-purple-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="flex-1 flex flex-col p-8 text-left bg-gray-50/30">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h2 className="text-2xl font-bold" style={{ color: 'var(--text-h)' }}>
            Panel Scrum Mastera
          </h2>
          <p className="text-sm opacity-60">Zarządzanie sprintami i zadaniami</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setIsAddSprintModalOpen(true)}
            className="px-4 py-2 rounded-md font-bold text-sm text-white cursor-pointer hover:opacity-90 transition-opacity"
            style={{ backgroundColor: 'var(--accent)' }}
          >
            Dodaj sprint
          </button>

          <button
            onClick={() => navigate('/login')}
            className="px-4 py-2 rounded-md border text-sm font-medium cursor-pointer"
            style={{ borderColor: 'var(--border)', backgroundColor: 'var(--bg)' }}
          >
            Wyloguj
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-4">
          <h3 className="font-bold mb-2">Sprinty</h3>
          {sprints.map((sprint) => {
            const isSelected = selectedSprintId === sprint.id;
            return (
              <div
                key={sprint.id}
                onClick={() => setSelectedSprintId(sprint.id)}
                className={`p-6 rounded-xl border relative cursor-pointer transition-all ${
                  isSelected 
                    ? 'ring-2 ring-purple-500 shadow-md' 
                    : 'hover:bg-gray-50/50'
                }`}
                style={{ backgroundColor: 'var(--bg)', borderColor: isSelected ? 'var(--accent)' : 'var(--border)' }}
              >
                <h2 className="text-xl font-bold mb-1">{sprint.name}</h2>
                <p className="text-sm opacity-60">Status: <span className="font-medium">{sprint.status}</span></p>

                {(sprint.startDate || sprint.endDate) && (
                  <p className="text-xs font-medium opacity-60 mt-2">
                    🗓️ {sprint.startDate || '?'} - {sprint.endDate || '?'}
                  </p>
                )}

                <div className="absolute top-4 right-4 flex gap-1">
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); setEditingSprintId(sprint.id); }}
                    className="px-2 py-1 rounded-md text-xs border border-transparent hover:bg-gray-100 hover:text-gray-900 transition-colors cursor-pointer"
                    style={{ borderColor: 'var(--border)' }}
                  >
                    Edytuj
                  </button>
                  <button
                    type="button"
                    onClick={(e) => handleDeleteSprint(e, sprint.id)}
                    className="px-2 py-1 rounded-md text-xs text-red-500 border border-transparent hover:bg-red-100 hover:border-red-300 hover:text-red-700 transition-colors cursor-pointer"
                  >
                    Usuń
                  </button>
                </div>
              </div>
            );
            })}
            {sprints.length === 0 && (
              <p className="text-sm opacity-50 italic">Brak utworzonych sprintów.</p>
            )}
        </div>

        <div
          className="lg:col-span-2 p-6 rounded-xl border"
          style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
        >
          <h3 className="font-bold mb-4">Zadania w sprincie</h3>

          <form onSubmit={handleAddTask} className="flex gap-3 mb-6">
            <input
              value={newTask}
              onChange={(e) => setNewTask(e.target.value)}
              placeholder="Tytuł zadania"
              className="flex-1 px-4 py-2 rounded border"
              style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
            />

            <button
            type="submit"
              className="px-4 py-2 rounded font-bold text-white cursor-pointer"
              style={{ backgroundColor: 'var(--accent)' }}
            >
              Dodaj
            </button>
          </form>

          <div className="space-y-3">
            <div className="space-y-3">
            {tasks
              .filter((task) => task.sprintId === selectedSprintId)
              .map((task) => (
                <div
                key={task.id}
                className="p-4 rounded-lg border flex justify-between items-start"
                style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
              >
                <div>
                  <p className="font-bold text-lg mb-2">{task.title}</p>
                  
                  <p className="text-sm opacity-60 mb-3">
                    Przypisane do: {task.assignedTo.length > 0 ? task.assignedTo.join(', ') : 'Brak'}
                  </p>
                  
                  <div className="space-y-1">
                    <p className="text-sm opacity-80">
                      Status: <span className={`ml-1 ${getStatusColor(task.status)}`}>{task.status}</span>
                    </p>
                    
                    <p className="text-sm opacity-80">
                      Priorytet: <span className={`ml-1 ${getPriorityColor(task.priority)}`}>{task.priority}</span>
                    </p>

                    <p className="text-sm opacity-80">
                      Typ: <span className={`ml-1 ${getTypeColor(task.type)}`}>{task.type}</span>
                    </p>
                  </div>
                </div>
                <div className="flex flex-col gap-2 items-end">
                  <button
                    type="button"
                    onClick={() => setEditingTaskId(task.id)}
                    className="px-3 py-1.5 rounded-md text-sm font-medium border hover:bg-gray-100 transition-colors cursor-pointer hover:text-gray-900"
                    style={{ borderColor: 'var(--border)' }}
                  >
                    Edytuj
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDeleteTask(task.id)}
                    className="px-2 py-1 rounded-md text-xs text-red-500 border border-transparent hover:bg-red-100 hover:border-red-300 hover:text-red-700 transition-colors cursor-pointer"
                  >
                    Usuń
                  </button>
                </div>
              </div>
              ))}

            {tasks.filter((t) => t.sprintId === selectedSprintId).length === 0 && (
              <div className="text-center py-10 opacity-40 text-sm">
                Brak zadań w tym sprincie.
              </div>
            )}
            </div>
          </div>
        </div>
      </div>
      {editingTaskId && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div 
            className="w-full max-w-sm p-6 rounded-xl border shadow-2xl"
            style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-lg m-0" style={{ color: 'var(--text-h)' }}>
                Edytuj zadanie
              </h3>
              <button
                onClick={() => setEditingTaskId(null)}
                className="w-8 h-8 flex items-center justify-center rounded-md hover:bg-gray-100 transition-colors cursor-pointer opacity-50 hover:opacity-100 text-2xl"
                title="Zamknij"
                style={{ color: 'var(--text-h)' }}
              >
                &times;
              </button>
            </div>
            
            {/* Przypisane osoby */}
            <div className="mb-5">
              <h4 className="font-bold text-sm mb-2 opacity-70">Przypisane osoby:</h4>
              <div className="space-y-1">
                {teamMembers.map((member) => {
                  const activeTask = tasks.find((t) => t.id === editingTaskId);
                  const isAssigned = activeTask?.assignedTo.includes(member.name);

                  return (
                    <label 
                      key={member.id} 
                      className="flex items-center gap-3 p-1.5 rounded hover:bg-gray-50/50 cursor-pointer border border-transparent transition-colors"
                    >
                      <input
                        type="checkbox"
                        checked={isAssigned || false}
                        onChange={() => handleToggleAssignee(editingTaskId, member.name)}
                        className="w-4 h-4 cursor-pointer accent-blue-600"
                      />
                      <span className="font-medium text-sm">{member.name}</span>
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Status */}
            <div className="mb-6">
              <h4 className="font-bold text-sm mb-2 opacity-70">Status:</h4>
              <div className="flex flex-wrap gap-2">
                {[
                  { label: 'Do zrobienia', activeClass: 'bg-blue-100 text-blue-700 border-blue-400', dotColor: 'text-blue-500' },
                  { label: 'W trakcie', activeClass: 'bg-yellow-100 text-yellow-700 border-yellow-400', dotColor: 'text-yellow-500' },
                  { label: 'Ukończone', activeClass: 'bg-green-100 text-green-700 border-green-400', dotColor: 'text-green-500' }
                ].map((statusObj) => {
                  const currentStatus = tasks.find((t) => t.id === editingTaskId)?.status;
                  const isActive = currentStatus === statusObj.label;

                  return (
                    <button
                      key={statusObj.label}
                      onClick={() => handleChangeTaskStatus(editingTaskId, statusObj.label)}
                      className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer flex items-center ${
                        isActive 
                          ? statusObj.activeClass 
                          : 'bg-gray-50 text-gray-400 border-transparent hover:bg-gray-100 hover:text-gray-600'
                      }`}
                    >
                      <span className={`mr-1.5 text-[10px] ${isActive ? statusObj.dotColor : 'text-gray-400'}`}>●</span>
                      {statusObj.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Priorytet */}
            <div className="mb-8">
              <h4 className="font-bold text-sm mb-2 opacity-70">Priorytet:</h4>
              <div className="flex flex-wrap gap-2">
                {[
                  { label: 'Krytyczny', activeClass: 'bg-red-100 text-red-700 border-red-400', dotColor: 'text-red-500' },
                  { label: 'Pilny', activeClass: 'bg-orange-100 text-orange-700 border-orange-400', dotColor: 'text-orange-500' },
                  { label: 'Ważny', activeClass: 'bg-purple-100 text-purple-700 border-purple-400', dotColor: 'text-purple-500' },
                  { label: 'Neutralny', activeClass: 'bg-blue-100 text-blue-700 border-blue-500', dotColor: 'text-blue-300' }
                ].map((prioObj) => {
                  const currentPriority = tasks.find((t) => t.id === editingTaskId)?.priority;
                  const isActive = currentPriority === prioObj.label;

                  return (
                    <button
                      key={prioObj.label}
                      onClick={() => handleChangeTaskPriority(editingTaskId, prioObj.label)}
                      className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer flex items-center ${
                        isActive 
                          ? prioObj.activeClass 
                          : 'bg-gray-50 text-gray-400 border-transparent hover:bg-gray-100 hover:text-gray-600'
                      }`}
                    >
                      <span className={`mr-1.5 text-[10px] ${isActive ? prioObj.dotColor : 'text-gray-400'}`}>●</span>
                      {prioObj.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Typ */}
            <div className="mb-8">
              <h4 className="font-bold text-sm mb-2 opacity-70">Typ zadania:</h4>
              <div className="flex flex-wrap gap-2">
                {[
                  { label: 'Bug', activeClass: 'bg-red-100 text-red-700 border-red-400', dotColor: 'text-red-500' },
                  { label: 'Feature', activeClass: 'bg-blue-100 text-blue-700 border-blue-400', dotColor: 'text-blue-500' },
                  { label: 'Documentation', activeClass: 'bg-emerald-100 text-emerald-700 border-emerald-400', dotColor: 'text-green-500' },
                  { label: 'Question', activeClass: 'bg-purple-100 text-purple-700 border-purple-400', dotColor: 'text-purple-500' }
                ].map((typeObj) => {
                  const currentType = tasks.find((t) => t.id === editingTaskId)?.type;
                  const isActive = currentType === typeObj.label;

                  return (
                    <button
                      key={typeObj.label}
                      onClick={() => handleChangeTaskType(editingTaskId, typeObj.label)}
                      className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer flex items-center ${
                        isActive 
                          ? typeObj.activeClass 
                          : 'bg-gray-50 text-gray-400 border-transparent hover:bg-gray-100 hover:text-gray-600'
                      }`}
                    >
                      <span className={`mr-1.5 text-[10px] ${isActive ? typeObj.dotColor : 'text-gray-400'}`}>●</span>
                      {typeObj.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setEditingTaskId(null)}
                className="px-6 py-2 rounded-lg font-bold text-white cursor-pointer"
                style={{ backgroundColor: 'var(--accent)' }}
              >
                Gotowe
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Dodawanie sprintu */}
      {isAddSprintModalOpen && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div 
            className="w-full max-w-sm p-6 rounded-xl border shadow-2xl"
            style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
          >
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-lg m-0" style={{ color: 'var(--text-h)' }}>
                Dodaj nowy sprint
              </h3>
              <button
                onClick={() => setIsAddSprintModalOpen(false)}
                className="w-8 h-8 flex items-center justify-center rounded-md hover:bg-gray-100 transition-colors cursor-pointer opacity-50 hover:opacity-100 text-2xl"
                style={{ color: 'var(--text-h)' }}
              >
                &times;
              </button>
            </div>

            {/* Nazwa sprintu */}
            <form onSubmit={handleAddSprint}>
              <div className="mb-5">
                <h4 className="font-bold text-sm mb-2 opacity-70">Nazwa sprintu:</h4>
                <input
                  type="text"
                  value={newSprintName}
                  onChange={(e) => setNewSprintName(e.target.value)}
                  placeholder="Nazwa sprintu"
                  className="w-full px-4 py-2 rounded border focus:outline-none focus:ring-2"
                  style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
                  autoFocus
                />
              </div>

              {/* Kalendarz sprintu */}
              <div className="mb-5 flex gap-4">
                <div className="flex-1">
                  <h4 className="font-bold text-sm mb-2 opacity-70">Data rozpoczęcia:</h4>
                  <input
                    type="date"
                    value={newSprintStartDate}
                    onChange={(e) => setNewSprintStartDate(e.target.value)}
                    className="w-full px-4 py-2 rounded border focus:outline-none focus:ring-2 cursor-pointer text-sm"
                    style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
                  />
                </div>
                <div className="flex-1">
                  <h4 className="font-bold text-sm mb-2 opacity-70">Data zakończenia:</h4>
                  <input
                    type="date"
                    value={newSprintEndDate}
                    onChange={(e) => setNewSprintEndDate(e.target.value)}
                    className="w-full px-4 py-2 rounded border focus:outline-none focus:ring-2 cursor-pointer text-sm"
                    style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
                  />
                </div>
              </div>

              {/* Status sprintu */}
              <div className="mb-8">
                <h4 className="font-bold text-sm mb-2 opacity-70">Status:</h4>
                <div className="flex flex-wrap gap-2">
                  {[
                    { label: 'Planowany', activeClass: 'bg-gray-100 text-gray-700 border-gray-400', dotColor: 'text-gray-500' },
                    { label: 'Aktywny', activeClass: 'bg-blue-100 text-blue-700 border-blue-400', dotColor: 'text-blue-500' },
                    { label: 'Zakończony', activeClass: 'bg-green-100 text-green-700 border-green-400', dotColor: 'text-green-500' }
                  ].map((statusObj) => {
                    const isActive = newSprintStatus === statusObj.label;

                    return (
                      <button
                        type="button"
                        key={statusObj.label}
                        onClick={() => setNewSprintStatus(statusObj.label)}
                        className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer flex items-center ${
                          isActive 
                            ? statusObj.activeClass 
                            : 'bg-gray-50 text-gray-400 border-transparent hover:bg-gray-100 hover:text-gray-600'
                        }`}
                      >
                        <span className={`mr-1.5 text-[10px] ${isActive ? statusObj.dotColor : 'text-gray-400'}`}>●</span>
                        {statusObj.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="flex justify-end">
                <button
                  type="submit"
                  className="px-6 py-2 rounded-lg font-bold text-white cursor-pointer hover:opacity-90 transition-opacity"
                  style={{ backgroundColor: 'var(--accent)' }}
                >
                  Utwórz sprint
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edycja sprintu */}
      {editingSprintId && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div 
            className="w-full max-w-sm p-6 rounded-xl border shadow-2xl"
            style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
          >
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-lg m-0" style={{ color: 'var(--text-h)' }}>
                Edytuj sprint
              </h3>
              <button
                onClick={() => setEditingSprintId(null)}
                className="w-8 h-8 flex items-center justify-center rounded-md hover:bg-gray-100 transition-colors cursor-pointer opacity-50 hover:opacity-100 text-2xl"
                style={{ color: 'var(--text-h)' }}
              >
                &times;
              </button>
            </div>

            {/* Kalendarz sprintu */}
            <div className="mb-6 flex gap-4">
              <div className="flex-1">
                <h4 className="font-bold text-sm mb-2 opacity-70">Data rozpoczęcia:</h4>
                <input
                  type="date"
                  value={sprints.find((s) => s.id === editingSprintId)?.startDate || ''}
                  onChange={(e) => handleChangeSprintDate(editingSprintId, 'startDate', e.target.value)}
                  className="w-full px-3 py-2 rounded border focus:outline-none focus:ring-2 cursor-pointer text-sm"
                  style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
                />
              </div>
              <div className="flex-1">
                <h4 className="font-bold text-sm mb-2 opacity-70">Data zakończenia:</h4>
                <input
                  type="date"
                  value={sprints.find((s) => s.id === editingSprintId)?.endDate || ''}
                  onChange={(e) => handleChangeSprintDate(editingSprintId, 'endDate', e.target.value)}
                  className="w-full px-3 py-2 rounded border focus:outline-none focus:ring-2 cursor-pointer text-sm"
                  style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
                />
              </div>
            </div>

            {/* Status sprintu */}
            <div className="mb-8">
              <h4 className="font-bold text-sm mb-2 opacity-70">Status:</h4>
              <div className="flex flex-wrap gap-2">
                {[
                  { label: 'Planowany', activeClass: 'bg-gray-100 text-gray-700 border-gray-400', dotColor: 'text-gray-500' },
                  { label: 'Aktywny', activeClass: 'bg-blue-100 text-blue-700 border-blue-400', dotColor: 'text-blue-500' },
                  { label: 'Zakończony', activeClass: 'bg-green-100 text-green-700 border-green-400', dotColor: 'text-green-500' }
                ].map((statusObj) => {
                  const currentStatus = sprints.find((s) => s.id === editingSprintId)?.status;
                  const isActive = currentStatus === statusObj.label;

                  return (
                    <button
                      type="button"
                      key={statusObj.label}
                      onClick={() => handleChangeSprintStatus(editingSprintId, statusObj.label)}
                      className={`px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer flex items-center ${
                        isActive 
                          ? statusObj.activeClass 
                          : 'bg-gray-50 text-gray-400 border-transparent hover:bg-gray-100 hover:text-gray-600'
                      }`}
                    >
                      <span className={`mr-1.5 text-[10px] ${isActive ? statusObj.dotColor : 'text-gray-400'}`}>●</span>
                      {statusObj.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setEditingSprintId(null)}
                className="px-6 py-2 rounded-lg font-bold text-white cursor-pointer hover:opacity-90 transition-opacity"
                style={{ backgroundColor: 'var(--accent)' }}
              >
                Gotowe
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}