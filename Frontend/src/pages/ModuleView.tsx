import { useParams, Navigate } from "react-router-dom";
import { AppHeader } from "@/components/AppHeader";
import { AppSidebar } from "@/components/AppSidebar";
import { AgentInterface } from "@/components/AgentInterface";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { modules, SubTeam } from "@/data/modules";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { motion, useAnimation } from "framer-motion";
import { useEffect, useState } from "react";
import { Sparkles, Zap, ArrowRight, Users, Settings, BarChart } from "lucide-react";

export default function ModuleView() {
  const { moduleId, agentId } = useParams();
  const [isLoading, setIsLoading] = useState(true);
  const controls = useAnimation();

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
      controls.start("visible");
    }, 300);
    return () => clearTimeout(timer);
  }, [controls]);

  const module = modules.find((m) => m.id === moduleId);
  if (!module) {
    return <Navigate to="/404" replace />;
  }

  const allAgents = [
    ...(module.agents || []),
    ...(module.subTeams?.flatMap((st: SubTeam) => st.agents) || []),
  ];

  const agent = agentId ? allAgents.find((a) => a.id === agentId) : null;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
        ease: [0.4, 0, 0.2, 1] as const,
      },
    },
  };

  const cardVariants = {
    hidden: { y: 30, opacity: 0, scale: 0.95 },
    visible: {
      y: 0,
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.6,
        ease: [0.4, 0, 0.2, 1] as const,
      },
    },
    hover: {
      y: -8,
      scale: 1.02,
      transition: {
        duration: 0.3,
        ease: [0.4, 0, 0.2, 1] as const,
      },
    },
  };

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
              <motion.div
                className="space-y-8"
                variants={containerVariants}
                initial="hidden"
                animate={controls}
              >
                {/* Hero Section */}
                <motion.div 
                  className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/5 via-accent/5 to-secondary/5 border border-border/50 p-8"
                  variants={itemVariants}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-accent/10 opacity-20" />
                  <div className="relative z-10 space-y-4">
                    <div className="flex items-center gap-4">
                      <motion.div 
                        className="p-3 rounded-xl bg-primary/10 text-primary"
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        transition={{ duration: 0.2 }}
                      >
                        <module.icon className="w-8 h-8" />
                      </motion.div>
                      <div className="space-y-1">
                        <motion.h1 
                          className="text-4xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent"
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.6, delay: 0.2 }}
                        >
                          {module.title}
                        </motion.h1>
                        <motion.div 
                          className="flex items-center gap-2 text-sm text-muted-foreground"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.4 }}
                        >
                          <Sparkles className="w-4 h-4" />
                          <span>Financial Services Module</span>
                        </motion.div>
                      </div>
                    </div>
                    <motion.p 
                      className="text-lg text-muted-foreground leading-relaxed max-w-4xl"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.3 }}
                    >
                      {module.description}
                    </motion.p>
                    
                    {/* Stats */}
                    <motion.div 
                      className="flex items-center gap-6 pt-4"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.5 }}
                    >
                      <div className="flex items-center gap-2 text-sm">
                        <Users className="w-4 h-4 text-primary" />
                        <span className="font-medium">{allAgents.length}</span>
                        <span className="text-muted-foreground">Agents</span>
                      </div>
                      {module.subTeams && (
                        <div className="flex items-center gap-2 text-sm">
                          <Settings className="w-4 h-4 text-accent" />
                          <span className="font-medium">{module.subTeams.length}</span>
                          <span className="text-muted-foreground">Teams</span>
                        </div>
                      )}
                      <div className="flex items-center gap-2 text-sm">
                        <BarChart className="w-4 h-4 text-success" />
                        <span className="font-medium">Active</span>
                        <span className="text-muted-foreground">Status</span>
                      </div>
                    </motion.div>
                  </div>
                </motion.div>

                {/* Flat agents, if any */}
                {module.agents && module.agents.length > 0 && (
                  <motion.div className="space-y-6" variants={itemVariants}>
                    <div className="flex items-center gap-3">
                      <motion.div 
                        className="p-2 rounded-lg bg-primary/10 text-primary"
                        whileHover={{ scale: 1.1 }}
                      >
                        <Zap className="w-5 h-5" />
                      </motion.div>
                      <h2 className="text-2xl font-bold text-foreground">Direct Agents</h2>
                      <Badge variant="secondary" className="ml-auto">
                        {module.agents.length} agents
                      </Badge>
                    </div>
                    <motion.div 
                      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                      variants={containerVariants}
                    >
                      {module.agents.map((agent, index) => (
                        <motion.div
                          key={agent.id}
                          variants={cardVariants}
                          whileHover="hover"
                          custom={index}
                        >
                          <Card
                            className="group cursor-pointer border-0 shadow-lg bg-gradient-to-br from-card to-card/80 backdrop-blur-sm hover:shadow-2xl transition-all duration-300 overflow-hidden"
                            onClick={() =>
                              (window.location.href = `/module/${moduleId}/${agent.id}`)
                            }
                          >
                            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                            <CardHeader className="relative z-10 pb-4">
                              <div className="flex items-start justify-between">
                                <div className="space-y-2 flex-1">
                                  <CardTitle className="text-lg font-semibold group-hover:text-primary transition-colors duration-200">
                                    {agent.name}
                                  </CardTitle>
                                  <CardDescription className="text-sm text-muted-foreground line-clamp-2">
                                    {agent.description}
                                  </CardDescription>
                                </div>
                                <motion.div
                                  className="p-2 rounded-lg bg-primary/10 text-primary opacity-0 group-hover:opacity-100 transition-all duration-200"
                                  whileHover={{ scale: 1.1 }}
                                >
                                  <ArrowRight className="w-4 h-4" />
                                </motion.div>
                              </div>
                            </CardHeader>
                            <CardContent className="relative z-10 pt-0">
                              <div className="space-y-3">
                                <div className="text-sm">
                                  <span className="font-medium text-foreground">
                                    Outputs:
                                  </span>
                                  <div className="mt-2 flex flex-wrap gap-1.5">
                                    {agent.outputs.slice(0, 3).map((output, index) => (
                                      <Badge
                                        key={index}
                                        variant="outline"
                                        className="text-xs px-2 py-1 border-primary/20 bg-primary/5 text-primary hover:bg-primary/10 transition-colors"
                                      >
                                        {output}
                                      </Badge>
                                    ))}
                                    {agent.outputs.length > 3 && (
                                      <Badge
                                        variant="outline"
                                        className="text-xs px-2 py-1 border-muted text-muted-foreground"
                                      >
                                        +{agent.outputs.length - 3} more
                                      </Badge>
                                    )}
                                  </div>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        </motion.div>
                      ))}
                    </motion.div>
                  </motion.div>
                )}

                {/* Sub-teams with nested agents */}
                {module.subTeams?.length > 0 && (
                  <motion.div className="space-y-8" variants={itemVariants}>
                    {module.subTeams.map((st: SubTeam, teamIndex: number) => (
                      <motion.div 
                        key={st.id} 
                        className="space-y-6"
                        variants={itemVariants}
                        custom={teamIndex}
                      >
                        <div className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-r from-accent/10 to-primary/10 border border-border/50">
                          <motion.div 
                            className="p-3 rounded-xl bg-accent/20 text-accent"
                            whileHover={{ scale: 1.1, rotate: 5 }}
                          >
                            <Users className="w-6 h-6" />
                          </motion.div>
                          <div className="flex-1">
                            <h2 className="text-2xl font-bold text-foreground">
                              {st.name}
                            </h2>
                            {st.mode && (
                              <Badge 
                                variant="outline" 
                                className="mt-1 border-accent/30 text-accent bg-accent/10"
                              >
                                {st.mode} Mode
                              </Badge>
                            )}
                          </div>
                          <Badge variant="secondary" className="text-sm">
                            {st.agents.length} agents
                          </Badge>
                        </div>
                        
                        <motion.div 
                          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                          variants={containerVariants}
                        >
                          {st.agents.map((a, agentIndex: number) => (
                            <motion.div
                              key={a.id}
                              variants={cardVariants}
                              whileHover="hover"
                              custom={agentIndex}
                            >
                              <Card
                                className="group cursor-pointer border-0 shadow-lg bg-gradient-to-br from-card to-card/80 backdrop-blur-sm hover:shadow-2xl transition-all duration-300 overflow-hidden"
                                onClick={() =>
                                  (window.location.href = `/module/${moduleId}/${a.id}`)
                                }
                              >
                                <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                                <CardHeader className="relative z-10 pb-4">
                                  <div className="flex items-start justify-between">
                                    <div className="space-y-2 flex-1">
                                      <CardTitle className="text-lg font-semibold group-hover:text-accent transition-colors duration-200">
                                        {a.name}
                                      </CardTitle>
                                      <CardDescription className="text-sm text-muted-foreground line-clamp-2">
                                        {a.description}
                                      </CardDescription>
                                    </div>
                                    <motion.div
                                      className="p-2 rounded-lg bg-accent/10 text-accent opacity-0 group-hover:opacity-100 transition-all duration-200"
                                      whileHover={{ scale: 1.1 }}
                                    >
                                      <ArrowRight className="w-4 h-4" />
                                    </motion.div>
                                  </div>
                                </CardHeader>
                                <CardContent className="relative z-10 pt-0">
                                  <div className="space-y-3">
                                    <div className="text-sm">
                                      <span className="font-medium text-foreground">
                                        Outputs:
                                      </span>
                                      <div className="mt-2 flex flex-wrap gap-1.5">
                                        {a.outputs.slice(0, 3).map((output: string, index: number) => (
                                          <Badge
                                            key={index}
                                            variant="outline"
                                            className="text-xs px-2 py-1 border-accent/20 bg-accent/5 text-accent hover:bg-accent/10 transition-colors"
                                          >
                                            {output}
                                          </Badge>
                                        ))}
                                        {a.outputs.length > 3 && (
                                          <Badge
                                            variant="outline"
                                            className="text-xs px-2 py-1 border-muted text-muted-foreground"
                                          >
                                            +{a.outputs.length - 3} more
                                          </Badge>
                                        )}
                                      </div>
                                    </div>
                                  </div>
                                </CardContent>
                              </Card>
                            </motion.div>
                          ))}
                        </motion.div>
                      </motion.div>
                    ))}
                  </motion.div>
                )}
              </motion.div>
            )}
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}