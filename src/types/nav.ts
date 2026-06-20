// Shape of the `nav` metadata exported by page files, read via import.meta.glob.
export type NavModule = {
  nav?: {
    order: number;
    title: string;
    image?: string;
    tile?: boolean;
  };
};
