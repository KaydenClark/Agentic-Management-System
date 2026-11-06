// Types for flow.mjs, the one data file /start reads.

export type Holder = "owner" | "agent" | "returned" | "done";

export type Source = { label: string; path: string };

// A way out of a stage: the reader's button label and the stage it leads to.
export type Choice = { label: string; to: string };

export type Stage = {
  id: string;
  name: string;
  holder: Holder;
  line: string;
  sources: readonly Source[];
  // The usual way on. Absent on the last stage.
  next?: Choice;
  // Where the system really branches: the choice that sends work back.
  back?: Choice;
  // Off the main path (the returned loop).
  branch?: boolean;
};

export declare const HOLDERS: Record<Holder, { label: string; ball: string; meaning: string; hue: string }>;
export declare const SOURCES: Record<
  | "blueprint" | "runbook" | "agents" | "glossary"
  | "ddr000A" | "ddr000F" | "ddr000G" | "ddr000H" | "ddr000M" | "ddr000Y"
  | "adr000P" | "adr000Q" | "adr000R" | "adr001M" | "adr001K" | "adr001E" | "adr001H"
  | "adr002P" | "adr002W" | "adr002Z" | "adr003F",
  Source
>;
export declare const SAMPLE: string;
export declare const stages: readonly Stage[];
export declare const mainPath: readonly Stage[];
export declare const firstStage: Stage;
export declare const lastStage: Stage;
export declare function stageById(id: string): Stage;
export declare const ownerAlso: readonly { line: string; sources: readonly Source[] }[];
export declare const agentsAlso: readonly { line: string; sources: readonly Source[] }[];
export declare const orchestrators: readonly { id: string; name: string; does: string; never: string }[];
