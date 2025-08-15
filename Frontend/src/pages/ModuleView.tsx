import { useParams, Navigate } from "react-router-dom";
import { AppHeader } from "@/components/AppHeader";
import { AppSidebar } from "@/components/AppSidebar";
import { AgentInterface } from "@/components/AgentInterface";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { modules } from "@/data/modules";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ModuleView() {
  const { moduleId, agentId } = useParams();
  
  const module = modules.find(m => m.id === moduleId);
  if (!module) {
    return <Navigate to="/404" replace />;
  }

  const agent = agentId ? module.agents?.find(a => a.id === agentId) : null;

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
                  <h1 className="text-3xl font-bold text-foreground">{module.title}</h1>
                  <p className="text-lg text-muted-foreground">{module.description}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {module.agents?.map((agent) => (
                    <Card 
                      key={agent.id} 
                      className="cursor-pointer hover:shadow-card-hover transition-all duration-200 hover:-translate-y-1"
                      onClick={() => window.location.href = `/module/${moduleId}/${agent.id}`}
                    >
                      <CardHeader>
                        <CardTitle className="text-lg">{agent.name}</CardTitle>
                        <CardDescription>{agent.description}</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          <div className="text-sm">
                            <span className="font-medium text-foreground">Outputs:</span>
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
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}