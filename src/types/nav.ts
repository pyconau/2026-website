// Shape of the `nav` metadata exported by page files, read via import.meta.glob.
export type NavModule = {
  nav?: {
    order: number;
    title: string;
    image?: string;
    tile?: boolean;
    /** Optional side-nav grouping heading, e.g. "Before PyCon AU". */
    group?: string;
    /** Highlight this item in the nav with the flourish motif, in this colour. */
    flourish?: "emerald" | "violet";
  };
};
