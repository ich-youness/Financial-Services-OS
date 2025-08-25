import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface ModuleCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  colorClass: string;
  onClick: () => void;
}

export function ModuleCard({ title, description, icon: Icon, colorClass, onClick }: ModuleCardProps) {
  return (
    <motion.div 
      className="group cursor-pointer"
      whileHover={{ 
        y: -8, 
        scale: 1.02,
        transition: { duration: 0.2 }
      }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
    >
      <div className={cn(
        "relative overflow-hidden rounded-2xl bg-gradient-to-br from-card to-card/80 border border-border/50 shadow-lg hover:shadow-2xl transition-all duration-300 backdrop-blur-sm p-8 h-80 flex flex-col",
        colorClass
      )}>
        {/* Background Effect */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Content */}
        <div className="relative z-10 flex flex-col h-full">
          <div className="flex items-start gap-6 flex-1">
            <motion.div 
              className="flex-shrink-0 p-4 rounded-2xl bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors duration-200"
              whileHover={{ scale: 1.1, rotate: 5 }}
              transition={{ duration: 0.2 }}
            >
              <Icon className="w-8 h-8" />
            </motion.div>
            
            <div className="flex-1 flex flex-col justify-between min-h-0">
              <div className="space-y-3">
                <h3 className="text-xl font-bold text-foreground group-hover:text-primary transition-colors duration-200 line-clamp-2 leading-tight">
                  {title}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed line-clamp-4">
                  {description}
                </p>
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
            <ArrowRight className="w-4 h-4" />
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}