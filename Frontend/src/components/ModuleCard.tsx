import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface ModuleCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  colorClass: string;
  onClick: () => void;
}

export function ModuleCard({ title, description, icon: Icon, colorClass, onClick }: ModuleCardProps) {
  return (
    <div 
      className={cn("module-card", colorClass)}
      onClick={onClick}
    >
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 rounded-lg bg-muted/50 flex items-center justify-center">
            <Icon className="w-6 h-6 text-foreground" />
          </div>
        </div>
        <div className="flex-1 space-y-2">
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
          <p className="text-sm text-muted-foreground text-balance leading-relaxed">
            {description}
          </p>
        </div>
      </div>
    </div>
  );
}