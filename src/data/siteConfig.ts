/**
 * Site configuration for temporary rebranding
 * Set KIWIPYCON_ENABLED to true to activate "Kiwi PyCon | West Island" branding
 */

export const KIWIPYCON_ENABLED = true;

export const siteConfig = {
  // Default branding
  default: {
    name: "PyCon AU",
    fullName: "PyCon AU 2026",
    tagline: "More than a Python conference",
    navLogo: "/images/logo.svg",
    navLogoDark: "/images/logo.svg",
  },
  // Kiwi PyCon branding
  kiwiPyCon: {
    name: "Kiwi PyCon West Island",
    fullName: "Kiwi PyCon West Island 2026",
    tagline: "More than a Python conference",
    navLogo: "/images/pyconau26_laser_kiwi.svg",
    navLogoDark: "/images/pyconau26_laser_kiwi_stone.svg",
  },
};

// Helper to get current branding
export const getBranding = () => {
  return KIWIPYCON_ENABLED ? siteConfig.kiwiPyCon : siteConfig.default;
};
