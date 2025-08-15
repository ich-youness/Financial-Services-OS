import { useNavigate } from "react-router-dom";
import { AppHeader } from "@/components/AppHeader";
import { ModuleCard } from "@/components/ModuleCard";
import { modules } from "@/data/modules";

const Index = () => {
  const navigate = useNavigate();

  const handleModuleClick = (moduleId: string) => {
    navigate(`/module/${moduleId}`);
  };

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      
      <main className="container mx-auto px-6 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-foreground mb-4">
            Financial Services Operating System
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto text-balance">
            Comprehensive AI-powered platform for risk assessment, investment analysis, 
            client management, fraud detection, compliance monitoring, and customer support.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {modules.map((module) => (
            <ModuleCard
              key={module.id}
              title={module.title}
              description={module.description}
              icon={module.icon}
              colorClass={module.colorClass}
              onClick={() => handleModuleClick(module.id)}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default Index;
