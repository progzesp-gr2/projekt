/**
 * To jest plik, który dostarcza backlog
 * Należy dodać endpoint do zmiany priorytetu zadania (opisałem to poniżej :) )
 */

import { useState } from 'react';

export default function BacklogTab({projectId}) {

  const [editingTaskId, setEditingTaskId] = useState(null);

  const [tasks, setTasks] = useState([
    {
        id: 1,
        title: 'Login page',
        assignedTo: 'Jan Kowalski',
        priority: 'to_set',
    },
    {
        id: 2,
        title: 'Dashboard UI',
        assignedTo: 'Anna Nowak',
        priority: 'high',
    },
    {
        id: 3,
        title: 'Fix navbar',
        assignedTo: 'Piotr Zielinski',
        priority: 'medium',
    },
  ]);

  // DLA BACKENDU wystarczy dać tu endpoint coś w stylu:
  //await axios.put('/api/task/priority', ...)
  const handlePriorityChange = (taskId, newPriority) => {
    setTasks((prevTasks) =>
        prevTasks.map((task) =>
        task.id === taskId
            ? { ...task, priority: newPriority }
            : task
        )
    );
  };

  

  const getPriorityStyle = (priority) => {
    switch (priority.toLowerCase()) {

        case 'to_set':
        return 'bg-gray-100 text-gray-700 border-gray-200';

        case 'critical':
        return 'bg-red-100 text-red-700 border-red-200';

        case 'high':
        return 'bg-orange-100 text-orange-700 border-orange-200';

        case 'medium':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';

        case 'normal':
        return 'bg-green-100 text-green-700 border-green-200';

        default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  return (
    <div className="p-6">

      <div className="flex justify-between items-center mb-6">
        <h2
          className="text-2xl font-bold"
          style={{ color: 'var(--text-h)' }}
        >
          Product Backlog
        </h2>

        <button
          className="px-4 py-2 rounded-lg text-white font-bold cursor-pointer"
          style={{ backgroundColor: 'var(--accent)' }}
        >
          + Add Task
        </button>
      </div>

        <div className="space-y-4">

         {tasks.map((task) => (
            <div
                key={task.id}
                className="p-5 rounded-xl border flex justify-between items-center"
                style={{
                    backgroundColor: 'var(--code-bg)',
                    borderColor: 'var(--border)',
                }}
                >

                <div>
                    <h3 className="font-bold text-lg">
                    {task.title}
                    </h3>

                    <p className="text-sm opacity-60">
                    Responsible: {task.assignedTo}
                    </p>
                </div>

                <div className="flex items-center gap-4">

                    {/* PRIORITY */}
                    {editingTaskId === task.id ? (
                    <select
                        value={task.priority}
                        onChange={(e) =>
                        handlePriorityChange(task.id, e.target.value)
                        }
                        className="px-3 py-2 rounded border"
                        style={{
                        backgroundColor: 'var(--bg)',
                        borderColor: 'var(--border)',
                        }}
                    >
                        <option value="to_set">To Set</option>
                        <option value="critical">Critical</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="normal">Normal</option>
                    </select>
                    ) : (
                    <span
                        className={`px-3 py-1 rounded-full text-xs font-bold border ${getPriorityStyle(task.priority)}`}
                    >
                        {task.priority}
                    </span>
                    )}

                    {/* BUTTON */}
                    {editingTaskId === task.id ? (
                    <button
                        onClick={() => setEditingTaskId(null)}
                        className="px-3 py-2 rounded text-white font-bold cursor-pointer"
                        style={{ backgroundColor: 'var(--accent)' }}
                    >
                        Save
                    </button>
                    ) : (
                    <button
                        onClick={() => setEditingTaskId(task.id)}
                        className="px-3 py-2 rounded border font-bold cursor-pointer"
                        style={{
                        borderColor: 'var(--border)',
                        }}
                    >
                        Edit
                    </button>
                    )}

                </div>

            </div>
            ))}

        </div>
    </div>
  );
}