/**
 * Panel zarządzania projektami:
 * - tworzenie projektów
 * - dodawanie programistów
 * 
 * To jest wyświetlane kiedy product owner będzie chciał dodać projekt.
 */

export default function ProjectManagementPanel({
  programmers,
  selectedProject,

  newProjectName,
  setNewProjectName,

  newProjectDescription,
  setNewProjectDescription,

  handleCreateProject,
  handleAddProgrammer,
}) {

  return (
    <div className="space-y-6">
      <form
        onSubmit={handleCreateProject}
        className="p-5 rounded-xl border"
        style={{
          backgroundColor: 'var(--bg)',
          borderColor: 'var(--border)',
          boxShadow: 'var(--shadow)',
        }}
      >

        <h3 className="font-bold mb-4">
          Utwórz nowy projekt
        </h3>

        <input
          type="text"
          value={newProjectName}
          onChange={(e) =>
            setNewProjectName(e.target.value)
          }
          placeholder="Nazwa projektu"
          className="w-full px-4 py-2 mb-3 rounded border"
          style={{
            backgroundColor: 'var(--code-bg)',
            borderColor: 'var(--border)',
          }}
        />

        <textarea
          value={newProjectDescription}
          onChange={(e) =>
            setNewProjectDescription(e.target.value)
          }
          placeholder="Opis projektu"
          rows="3"
          className="w-full px-4 py-2 mb-3 rounded border resize-none"
          style={{
            backgroundColor: 'var(--code-bg)',
            borderColor: 'var(--border)',
          }}
        />

        <button
          type="submit"
          className="w-full py-2 rounded-lg font-bold text-white cursor-pointer"
          style={{
            backgroundColor: 'var(--accent)',
          }}
        >
          Dodaj projekt
        </button>

      </form>

      <div
        className="p-5 rounded-xl border"
        style={{
          backgroundColor: 'var(--bg)',
          borderColor: 'var(--border)',
          boxShadow: 'var(--shadow)',
        }}
      >

        <h3 className="font-bold mb-4">
          Dodaj programistę
        </h3>

        {!selectedProject ? (
          <p className="text-sm opacity-60">
            Wybierz projekt
          </p>

        ) : (

          <div className="space-y-3">
            {programmers.map((programmer) => {

              const alreadyAdded =
                selectedProject.members.some(
                  (member) =>
                    member.id === programmer.id
                );

              return (
                <div
                  key={programmer.id}
                  className="p-3 rounded border flex justify-between items-center"
                  style={{
                    borderColor: 'var(--border)',
                  }}
                >

                  <div>
                    <p className="font-bold text-sm">
                      {programmer.name}
                    </p>

                    <p className="text-xs opacity-60">
                      {programmer.email}
                    </p>

                  </div>

                  <button
                    onClick={() =>
                      handleAddProgrammer(
                        selectedProject.id,
                        programmer
                      )
                    }
                    disabled={alreadyAdded}
                    className={`px-3 py-1 rounded text-xs font-bold text-white ${
                      alreadyAdded
                        ? 'opacity-40 cursor-not-allowed'
                        : 'cursor-pointer'
                    }`}
                    style={{
                      backgroundColor: 'var(--accent)',
                    }}
                  >
                    {alreadyAdded
                      ? 'Dodany'
                      : 'Dodaj'}
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}