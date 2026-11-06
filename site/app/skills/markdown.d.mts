// Types for markdown.mjs, the skills wiki's restricted Markdown.

export type Inline =
  | { type: "text"; value: string }
  | { type: "code"; value: string }
  | { type: "strong"; children: Inline[] }
  | { type: "em"; children: Inline[] }
  | { type: "link"; href: string; children: Inline[] };

export type Block =
  | { type: "heading"; level: 2 | 3; inline: Inline[]; line: number }
  | { type: "paragraph"; inline: Inline[] }
  | { type: "list"; ordered: boolean; items: Inline[][] }
  | { type: "table"; header: Inline[][]; rows: Inline[][][] }
  | { type: "blockquote"; paragraphs: Inline[][] }
  | { type: "code"; lang: string | null; text: string };

export declare class MarkdownError extends Error {
  file: string;
  line: number;
}

export declare function inlineText(nodes: readonly Inline[]): string;
export declare function slug(text: string): string;
export declare function parseInline(src: string, fail: (message: string) => never, inLink?: boolean): Inline[];
export declare function parseMarkdown(src: string, file?: string, firstLine?: number): Block[];
