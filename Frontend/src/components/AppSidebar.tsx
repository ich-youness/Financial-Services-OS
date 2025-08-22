import { useState, useEffect, useRef } from "react";
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
  const [expandedSubTeams, setExpandedSubTeams] = useState<Record<string, boolean>>({});

  // Resizable width state (persisted)
  const DEFAULT_WIDTH = 260;
  const MIN_WIDTH = 260;
  const MAX_WIDTH = 440;
  const [sidebarWidth, setSidebarWidth] = useState<number>(() => {
    try {
      const stored = typeof window !== 'undefined' ? localStorage.getItem('sidebarWidth') : null;
      const parsed = stored ? parseInt(stored, 10) : NaN;
      return Number.isFinite(parsed) ? parsed : DEFAULT_WIDTH;
    } catch {
      return DEFAULT_WIDTH;
    }
  });
  const widthRef = useRef<number>(sidebarWidth);
  useEffect(() => { widthRef.current = sidebarWidth; }, [sidebarWidth]);

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

  const toggleSubTeam = (subTeamKey: string) => {
    setExpandedSubTeams(prev => ({ ...prev, [subTeamKey]: !prev[subTeamKey] }));
  };

  const handleAgentSelect = (moduleId: string, agentId: string) => {
    navigate(`/module/${moduleId}/${agentId}`);
  };

  const startResize = (e: React.MouseEvent<HTMLDivElement>) => {
    if (collapsed) return;
    e.preventDefault();
    const startX = e.clientX;
    const startWidth = widthRef.current;

    const onMove = (ev: MouseEvent) => {
      const delta = ev.clientX - startX;
      const next = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, startWidth + delta));
      setSidebarWidth(next);
    };
    const onUp = () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
      try { localStorage.setItem('sidebarWidth', String(widthRef.current)); } catch {}
    };

    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
  };

  return (
    <Sidebar
      className={cn(
        collapsed ? "w-sidebar-collapsed" : "w-sidebar",
        "sticky top-0 h-screen"
      )}
      collapsible="icon"
      style={!collapsed ? { width: sidebarWidth } : undefined}
    >
      <SidebarContent className="h-full overflow-y-auto">
        <SidebarGroup>
          <SidebarGroupLabel>Modules</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {modules.map((module) => {
                const isExpanded = expandedModules.includes(module.id);
                const isModuleActive = currentModule === module.id;
                const hasSubTeams = Array.isArray((module as any).subTeams) && (module as any).subTeams.length > 0;
                const hasAgents = Array.isArray(module.agents) && module.agents.length > 0;
                
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
                        {!collapsed && (hasSubTeams || hasAgents) && (
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

                    {!collapsed && isExpanded && (
                      <div className="ml-6 space-y-1">
                        {hasSubTeams ? (
                          (module as any).subTeams.map((st: any) => {
                            const subKey = `${module.id}/${st.id}`;
                            const stExpanded = !!expandedSubTeams[subKey];
                            return (
                              <div key={st.id} className="space-y-1">
                                <div className="flex items-center w-full">
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    className="flex-1 justify-start gap-2 h-7 px-2"
                                    onClick={() => toggleSubTeam(subKey)}
                                  >
                                    {stExpanded ? (
                                      <ChevronDown className="h-3 w-3" />
                                    ) : (
                                      <ChevronRight className="h-3 w-3" />
                                    )}
                                    <span className="text-sm">{st.name}</span>
                                  </Button>
                                  {/* <span className="text-[10px] text-muted-foreground px-1">{st.mode}</span> */}
                                </div>
                                {stExpanded && (
                                  <div className="ml-5 space-y-1">
                                    {st.agents.map((agent: any) => {
                                      const isAgentActive = currentAgent === agent.id && currentModule === module.id;
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
                          })
                        ) : (
                          hasAgents && module.agents!.map((agent) => {
                            const isAgentActive = currentAgent === agent.id && currentModule === module.id;
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
                          })
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      {!collapsed && (
        <div
          onMouseDown={startResize}
          className="absolute right-0 top-0 h-full w-1 cursor-col-resize hover:bg-border"
        />
      )}
    </Sidebar>
  );
}