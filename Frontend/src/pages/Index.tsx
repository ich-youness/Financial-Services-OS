import { useNavigate } from "react-router-dom";
import { AppHeader } from "@/components/AppHeader";
import { ModuleCard } from "@/components/ModuleCard";
import { modules } from "@/data/modules";
import { motion, useAnimation } from "framer-motion";
import { useEffect, useState } from "react";
import { Sparkles, TrendingUp, Shield, ChevronRight, Play, Users, BarChart3 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const Index = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const controls = useAnimation();

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
      controls.start("visible");
    }, 200);
    return () => clearTimeout(timer);
  }, [controls]);

  const handleModuleClick = (moduleId: string) => {
    navigate(`/module/${moduleId}`);
  };

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
    hidden: { y: 30, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6,
        ease: [0.4, 0, 0.2, 1] as const,
      },
    },
  };

  const cardVariants = {
    hidden: { y: 40, opacity: 0, scale: 0.95 },
    visible: {
      y: 0,
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.7,
        ease: [0.4, 0, 0.2, 1] as const,
      },
    },
  };

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      
      <main className="relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-accent/5" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent" />
        
        <motion.div 
          className="relative z-10 container mx-auto px-6 py-16"
          variants={containerVariants}
          initial="hidden"
          animate={controls}
        >
          {/* Hero Section */}
          <motion.div className="text-center mb-20" variants={itemVariants}>
            <motion.div 
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6"
              variants={itemVariants}
            >
              <Sparkles className="w-4 h-4" />
              <span>Next-Generation Financial Platform</span>
            </motion.div>
            
            <motion.h1 
              className="text-5xl md:text-6xl lg:text-7xl font-bold bg-gradient-to-r from-foreground via-foreground to-foreground/70 bg-clip-text text-transparent mb-6 leading-tight"
              variants={itemVariants}
            >
              Financial Services
              <br />
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Operating System
              </span>
            </motion.h1>
            
            <motion.p 
              className="text-xl md:text-2xl text-muted-foreground max-w-4xl mx-auto text-balance leading-relaxed mb-8"
              variants={itemVariants}
            >
              Comprehensive AI-powered platform for risk assessment, investment analysis, 
              client management, fraud detection, compliance monitoring, and customer support.
            </motion.p>
            
            {/* Action Buttons */}
            <motion.div 
              className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12"
              variants={itemVariants}
            >
              <Button 
                size="lg" 
                className="bg-primary hover:bg-primary-hover text-primary-foreground px-8 py-6 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 group"
                onClick={() => navigate('/modules')}
              >
                <Play className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
                Explore Modules
                <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                className="px-8 py-6 text-lg font-semibold rounded-xl hover:bg-accent/10 border-2 transition-all duration-200"
              >
                <BarChart3 className="w-5 h-5 mr-2" />
                View Analytics
              </Button>
            </motion.div>
            
            {/* Stats */}
            <motion.div 
              className="flex flex-wrap items-center justify-center gap-8 text-sm"
              variants={itemVariants}
            >
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                <span className="font-medium">{modules.length}</span>
                <span className="text-muted-foreground">Active Modules</span>
              </div>
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-accent" />
                <span className="font-medium">50+</span>
                <span className="text-muted-foreground">AI Agents</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-success" />
                <span className="font-medium">Enterprise</span>
                <span className="text-muted-foreground">Security</span>
              </div>
            </motion.div>
          </motion.div>
          {/* Modules Section */}
          <motion.div className="space-y-8" variants={itemVariants}>
            <div className="text-center space-y-4">
              <motion.div 
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 text-accent text-sm font-medium"
                variants={itemVariants}
              >
                <TrendingUp className="w-4 h-4" />
                <span>Available Modules</span>
              </motion.div>
              <motion.h2 
                className="text-3xl md:text-4xl font-bold text-foreground"
                variants={itemVariants}
              >
                Choose Your Financial Domain
              </motion.h2>
              <motion.p 
                className="text-lg text-muted-foreground max-w-2xl mx-auto"
                variants={itemVariants}
              >
                Select from our comprehensive suite of AI-powered financial modules, 
                each designed to handle specific aspects of modern financial operations.
              </motion.p>
            </div>
            
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto"
              variants={containerVariants}
            >
              {modules.map((module, index) => (
                <motion.div
                  key={module.id}
                  variants={cardVariants}
                  custom={index}
                  whileHover={{ 
                    y: -8, 
                    scale: 1.02,
                    transition: { duration: 0.2 }
                  }}
                  whileTap={{ scale: 0.98 }}
                  className="group"
                >
                  <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-card to-card/80 border border-border/50 shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer backdrop-blur-sm h-80 flex flex-col"
                       onClick={() => handleModuleClick(module.id)}>
                    {/* Card Background Effect */}
                    <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    
                    {/* Content */}
                    <div className="relative z-10 p-8 flex flex-col h-full">
                      <div className="flex items-start gap-6 flex-1">
                        <motion.div 
                          className="flex-shrink-0 p-4 rounded-2xl bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors duration-200"
                          whileHover={{ scale: 1.1, rotate: 5 }}
                          transition={{ duration: 0.2 }}
                        >
                          <module.icon className="w-8 h-8" />
                        </motion.div>
                        
                        <div className="flex-1 flex flex-col justify-between min-h-0">
                          <div className="space-y-3">
                            <h3 className="text-xl font-bold text-foreground group-hover:text-primary transition-colors duration-200 line-clamp-2 leading-tight">
                              {module.title}
                            </h3>
                            <p className="text-sm text-muted-foreground leading-relaxed line-clamp-4">
                              {module.description}
                            </p>
                          </div>
                          
                          {/* Module Stats */}
                          <div className="flex items-center gap-2 mt-4 flex-wrap">
                            <Badge variant="secondary" className="text-xs">
                              {module.agents?.length || 0} agents
                            </Badge>
                            {module.subTeams && module.subTeams.length > 0 && (
                              <Badge variant="outline" className="text-xs border-primary/20 text-primary">
                                {module.subTeams.length} teams
                              </Badge>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      {/* Hover Arrow - Fixed at bottom */}
                      <motion.div 
                        className="flex items-center text-primary opacity-0 group-hover:opacity-100 transition-all duration-200 mt-4 pt-4 border-t border-border/20"
                        initial={{ x: -10 }}
                        whileHover={{ x: 0 }}
                      >
                        <span className="text-sm font-medium mr-2">Explore Module</span>
                        <ChevronRight className="w-4 h-4" />
                      </motion.div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
};

export default Index;
