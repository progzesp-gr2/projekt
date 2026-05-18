/**
 * Panel zarządzania projektami.
 *
 * Product Owner może:
 * - tworzyć projekty
 * - dodawać programistów do projektu
 *
 * Komponent wyświetlany tylko dla Product Ownera.
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

      {/* CREATE PROJECT */}
      <form
        onSubmit={handleCreateProject}
        className="p-5 rounded-xl border"
        style={{
          backgroundColor: 'var(--bg)',
          borderColor: 'var(--border)',
          boxShadow: 'var(--shadow)',
        }}
      >

        <div className="mb-5">

          <h3 className="font-bold text-lg">
            Utwórz nowy projekt
          </h3>

          <p className="text-sm opacity-60">
            Dodaj nowy projekt do systemu
          </p>

        </div>

        {/* PROJECT NAME */}
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

        {/* PROJECT DESCRIPTION */}
        <textarea
          value={newProjectDescription}
          onChange={(e) =>
            setNewProjectDescription(
              e.target.value
            )
          }
          placeholder="Opis projektu"
          rows="3"
          className="w-full px-4 py-2 mb-4 rounded border resize-none"
          style={{
            backgroundColor: 'var(--code-bg)',
            borderColor: 'var(--border)',
          }}
        />

        {/* SUBMIT */}
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

      {/* ADD PROGRAMMERS */}
      <div
        className="p-5 rounded-xl border"
        style={{
          backgroundColor: 'var(--bg)',
          borderColor: 'var(--border)',
          boxShadow: 'var(--shadow)',
        }}
      >

        <div className="mb-5">

          <h3 className="font-bold text-lg">
            Dodaj programistę
          </h3>

          <p className="text-sm opacity-60">
            Dodaj użytkowników do wybranego projektu
          </p>

        </div>

        {!selectedProject ? (

          <div
            className="p-4 rounded-lg border text-sm opacity-60"
            style={{
              borderColor: 'var(--border)',
              backgroundColor: 'var(--code-bg)',
            }}
          >
            Najpierw wybierz projekt z listy
          </div>

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
                    backgroundColor:
                      'var(--code-bg)',
                  }}
                >

                  {/* USER INFO */}
                  <div>

                    <p className="font-bold text-sm">
                      {programmer.name}
                    </p>

                    <p className="text-xs opacity-60">
                      {programmer.email}
                    </p>

                  </div>

                  {/* ADD BUTTON */}
                  <button
                    type="button"
                    onClick={() =>
                      handleAddProgrammer(
                        selectedProject.id,
                        programmer
                      )
                    }
                    disabled={alreadyAdded}
                    className={`px-3 py-1 rounded text-xs font-bold text-white transition-opacity ${
                      alreadyAdded
                        ? 'opacity-40 cursor-not-allowed'
                        : 'cursor-pointer hover:opacity-90'
                    }`}
                    style={{
                      backgroundColor:
                        'var(--accent)',
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