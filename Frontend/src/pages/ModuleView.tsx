import { useParams, Navigate } from "react-router-dom";
import { AppHeader } from "@/components/AppHeader";
import { AppSidebar } from "@/components/AppSidebar";
import { AgentInterface } from "@/components/AgentInterface";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { modules } from "@/data/modules";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function ModuleView() {
  const { moduleId, agentId } = useParams();

  const module = modules.find((m) => m.id === moduleId);
  if (!module) {
    return <Navigate to="/404" replace />;
  }

  const allAgents = [
    ...(module.agents || []),
    ...((module as any).subTeams?.flatMap((st: any) => st.agents) || []),
  ];

  const agent = agentId ? allAgents.find((a) => a.id === agentId) : null;

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar />

        <div className="flex-1 flex flex-col">
          <AppHeader />

          <main className="flex-1 p-6">
            {agent ? (
              <AgentInterface agent={agent} parentModule={module} />
            ) : (
              // Module overview page
              <div className="space-y-6">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold text-foreground">
                    {module.title}
                  </h1>
                  <p className="text-lg text-muted-foreground">
                    {module.description}
                  </p>
                </div>

                {/* Flat agents, if any */}
                {module.agents && module.agents.length > 0 && (
                  <div className="space-y-3">
                    <h2 className="text-xl font-semibold">Agents</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {module.agents.map((agent) => (
                        <Card
                          key={agent.id}
                          className="cursor-pointer hover:shadow-card-hover transition-all duration-200 hover:-translate-y-1"
                          onClick={() =>
                            (window.location.href = `/module/${moduleId}/${agent.id}`)
                          }
                        >
                          <CardHeader>
                            <CardTitle className="text-lg">
                              {agent.name}
                            </CardTitle>
                            <CardDescription>
                              {agent.description}
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                                <div className="space-y-2">
                                  <div className="text-sm">
                                    <span className="font-medium text- foreground">
                                      Outputs:
                                    </span>
                                    <div className="mt-1 flex flex-wrap gap-1">
                                      {agent.outputs.map((output, index) => (
                                        <span
                                          key={index}
                                          className="inline-block px-2 py-1 bg-muted text-muted-foreground text-xs rounded-md"
                                        >
                                          {output}
                                        </span>
                                      ))}
                                    </div>
                                  </div>{" "}
                                </div>
                              </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {/* Sub-teams with nested agents */}
                {(module as any).subTeams?.length > 0 && (
                  <div className="space-y-6">
                    {(module as any).subTeams.map((st: any) => (
                      <div key={st.id} className="space-y-3">
                        <h2 className="text-xl font-semibold flex items-center gap-2">
                          <span>{st.name}</span>
                          {/* <span className="text-xs text-muted-foreground">
                            ({st.mode})
                          </span> */}
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {st.agents.map((a: any) => (
                            <Card
                              key={a.id}
                              className="cursor-pointer hover:shadow-card-hover transition-all duration-200 hover:-translate-y-1"
                              onClick={() =>
                                (window.location.href = `/module/${moduleId}/${a.id}`)
                              }
                            >
                              <CardHeader>
                                <CardTitle className="text-lg">
                                  {a.name}
                                </CardTitle>
                                <CardDescription>
                                  {a.description}
                                </CardDescription>
                              </CardHeader>
                              <CardContent>
                                <div className="space-y-2">
                                  <div className="text-sm">
                                    <span className="font-medium text- foreground">
                                      Outputs:
                                    </span>
                                    <div className="mt-1 flex flex-wrap gap-1">
                                      {a.outputs.map((output, index) => (
                                        <span
                                          key={index}
                                          className="inline-block px-2 py-1 bg-muted text-muted-foreground text-xs rounded-md"
                                        >
                                          {output}
                                        </span>
                                      ))}
                                    </div>
                                  </div>{" "}
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}