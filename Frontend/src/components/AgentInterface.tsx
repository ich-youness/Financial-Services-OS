import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { Upload, Play, FileText, BarChart3, Table } from "lucide-react";
import { Agent } from "@/data/modules";
import { Module } from "@/data/modules";

interface AgentInterfaceProps {
  agent: Agent;
  parentModule: Module;
}


 export function AgentInterface({ agent, parentModule }: AgentInterfaceProps) {
  const [inputText, setInputText] = useState("");
  const [config, setConfig] = useState<Record<string, any>>({});
  const [isRunning, setIsRunning] = useState(false);
  const [output, setOutput] = useState<string | null>(null);

  const handleConfigChange = (key: string, value: any) => {
    setConfig(prev => ({ ...prev, [key]: value }));
  };

  // const handleRun = async () => {
  //   setIsRunning(true);
  //   // Simulate processing
  //   await new Promise(resolve => setTimeout(resolve, 2000));
  //   setOutput(`Processing completed for ${agent.name}. Results:\n\n${agent.outputs.join('\n')}\n\nInput: ${inputText}\nConfig: ${JSON.stringify(config, null, 2)}`);
  //   setIsRunning(false);
  // };

  const handleRun = async () => {
    setIsRunning(true);
    setOutput(null);

    // Build the final prompt
    const finalPrompt = `Module: ${parentModule.title}
Agent: ${agent.name}

${inputText}`;

    try {
      const res = await fetch("http://127.0.0.1:8000/module", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          moduleId: parentModule.id,
          agentId: agent.id,
          prompt: finalPrompt,
          config
        }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      // Display text result or dump JSON nicely
      const text =
        typeof data === "string"
          ? data
          : data.result ?? JSON.stringify(data, null, 2);

      setOutput(text || "No result returned from server.");
    } catch (err: any) {
      setOutput(`Error: ${err.message}`);
    } finally {
      setIsRunning(false);
    }
  };



  const renderConfigControl = (key: string, configItem: any) => {
    switch (configItem.type) {
      case 'dropdown':
        // return (
        //   <div key={key} className="space-y-2">
        //     <Label htmlFor={key}>{configItem.label}</Label>
        //     <Select onValueChange={(value) => handleConfigChange(key, value)}>
        //       <SelectTrigger>
        //         <SelectValue placeholder={`Select ${configItem.label}`} />
        //       </SelectTrigger>
        //       <SelectContent>
        //         {configItem.options?.map((option: string) => (
        //           <SelectItem key={option} value={option}>
        //             {option}
        //           </SelectItem>
        //         ))}
        //       </SelectContent>
        //     </Select>
        //   </div>
        // );
      
      case 'slider':
        // return (
          // <div key={key} className="space-y-3">
          //   <div className="flex items-center justify-between">
          //     <Label htmlFor={key}>{configItem.label}</Label>
          //     <span className="text-sm text-muted-foreground">
          //       {config[key] || configItem.default || configItem.min}
          //     </span>
          //   </div>
          //   <Slider
          //     id={key}
          //     min={configItem.min}
          //     max={configItem.max}
          //     step={0.1}
          //     value={[config[key] || configItem.default || configItem.min]}
          //     onValueChange={([value]) => handleConfigChange(key, value)}
          //   />
          // </div>
        // );
      
      case 'toggle':
        // return (
        //   <div key={key} className="flex items-center justify-between">
        //     <Label htmlFor={key}>{configItem.label}</Label>
        //     <Switch
        //       id={key}
        //       checked={config[key] || configItem.default || false}
        //       onCheckedChange={(checked) => handleConfigChange(key, checked)}
        //     />
        //   </div>
        // );
      
      case 'numeric':
        // return (
        //   <div key={key} className="space-y-2">
        //     <Label htmlFor={key}>{configItem.label}</Label>
        //     <Input
        //       id={key}
        //       type="number"
        //       placeholder={configItem.default?.toString() || "0"}
        //       value={config[key] || ""}
        //       onChange={(e) => handleConfigChange(key, parseFloat(e.target.value) || 0)}
        //     />
        //   </div>
        // );
      
      case 'text':
        // return (
        //   <div key={key} className="space-y-2">
        //     <Label htmlFor={key}>{configItem.label}</Label>
        //     <Input
        //       id={key}
        //       type="text"
        //       placeholder={configItem.default || ""}
        //       value={config[key] || ""}
        //       onChange={(e) => handleConfigChange(key, e.target.value)}
        //     />
        //   </div>
        // );
      
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Agent Header */}
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-foreground">{agent.name}</h2>
        <p className="text-muted-foreground">{agent.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
        {/* Input Area */}
        <Card className="agent-input-area">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Agent Input
            </CardTitle>
            <CardDescription>
              {agent.inputs.text}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-8">
            <div className="space-y-5">
              <Label htmlFor="input-text">Input Text</Label>
              <Textarea
                id="input-text"
                placeholder="Enter your data and parameters here..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                rows={4}
              />
            </div>
            
            {agent.inputs.fileUploads && (
              <div className="space-y-2">
                <Label>File Upload</Label>
                <div className="border-2 border-dashed border-border rounded-lg p-4">
                  <div className="flex flex-col items-center gap-2 text-center">
                    <Upload className="w-6 h-6 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">
                      Click to upload or drag and drop files
                    </p>
                    <Button variant="outline" size="sm">
                      Choose Files
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>


      </div>

      {/* Run Button */}
      <div className="flex justify-center">
        <Button 
          onClick={handleRun} 
          disabled={isRunning || !inputText.trim()}
          size="lg"
          className="gap-2"
        >
          <Play className="w-4 h-4" />
          {isRunning ? "Processing..." : "Run Analysis"}
        </Button>
      </div>

      {/* Output Display */}
      <Card className="output-display">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Output Results
          </CardTitle>
        </CardHeader>
        <CardContent>
          {output ? (
            <div className="space-y-4">
              <pre className="text-sm whitespace-pre-wrap bg-muted p-4 rounded-md overflow-x-auto">
                {output}
              </pre>
            </div>
          ) : (
            <div className="flex items-center justify-center py-12">
              <div className="text-center space-y-2">
                <Table className="w-8 h-8 text-muted-foreground mx-auto" />
                <p className="text-muted-foreground">
                  Run the analysis to see results here
                </p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}