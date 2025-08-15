import { useState } from "react";
import { ChevronRight, ChevronDown } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { modules } from "@/data/modules";

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();
  const navigate = useNavigate();
  const [expandedModules, setExpandedModules] = useState<string[]>([]);
  
  // Parse current route to get module and agent
  const pathParts = location.pathname.split('/');
  const currentModule = pathParts[2]; // /module/:moduleId/:agentId
  const currentAgent = pathParts[3];

  const toggleModule = (moduleId: string) => {
    setExpandedModules(prev => 
      prev.includes(moduleId) 
        ? prev.filter(id => id !== moduleId)
        : [...prev, moduleId]
    );
  };

  const handleAgentSelect = (moduleId: string, agentId: string) => {
    navigate(`/module/${moduleId}/${agentId}`);
  };

  return (
    <Sidebar className={collapsed ? "w-sidebar-collapsed" : "w-sidebar"} collapsible="icon">
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Modules</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {modules.map((module) => {
                const isExpanded = expandedModules.includes(module.id);
                const isModuleActive = currentModule === module.id;
                
                return (
                  <div key={module.id} className="space-y-1">
                    <SidebarMenuItem>
                      <div className="flex items-center w-full">
                        <Button
                          variant="ghost"
                          size="sm"
                          className={cn(
                            "flex-1 justify-start gap-2 h-8 px-2",
                            isModuleActive && "bg-accent text-accent-foreground"
                          )}
                          onClick={() => navigate(`/module/${module.id}`)}
                        >
                          <module.icon className="h-4 w-4" />
                          {!collapsed && <span className="text-sm">{module.title}</span>}
                        </Button>
                        {!collapsed && module.agents && module.agents.length > 0 && (
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-8 w-8 p-0 flex-shrink-0"
                            onClick={() => toggleModule(module.id)}
                          >
                            {isExpanded ? (
                              <ChevronDown className="h-3 w-3" />
                            ) : (
                              <ChevronRight className="h-3 w-3" />
                            )}
                          </Button>
                        )}
                      </div>
                    </SidebarMenuItem>
                    
                    {!collapsed && isExpanded && module.agents && (
                      <div className="ml-6 space-y-1">
                        {module.agents.map((agent) => {
                          const isAgentActive = currentAgent === agent.id;
                          return (
                            <SidebarMenuItem key={agent.id}>
                              <SidebarMenuButton
                                className={cn(
                                  "text-sm h-7 px-2",
                                  isAgentActive && "bg-accent text-accent-foreground"
                                )}
                                onClick={() => handleAgentSelect(module.id, agent.id)}
                              >
                                {agent.name}
                              </SidebarMenuButton>
                            </SidebarMenuItem>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}