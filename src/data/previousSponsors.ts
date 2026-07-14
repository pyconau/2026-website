/**
 * Previous sponsors from past PyCon AU conferences
 * Used as fallback when current year sponsors are not yet announced
 */

export interface PreviousSponsor {
  logo: string;
  alt: string;
  tier?: string;
}

export const previousSponsors: PreviousSponsor[] = [
  { logo: "previous/mongodb.svg", alt: "MongoDB", tier: "platinum" },
  { logo: "previous/snowflake.png", alt: "Snowflake", tier: "gold" },
  { logo: "previous/kraken-tech.png", alt: "Kraken Tech", tier: "gold" },
  { logo: "previous/psf.svg", alt: "The Python Software Foundation", tier: "gold" },
  { logo: "previous/cipherstash.svg", alt: "CipherStash", tier: "gold" },
  { logo: "previous/google.png", alt: "Google" },
  { logo: "previous/logo-elastic-horizontal-color.svg", alt: "Elastic" },
  { logo: "previous/microsoft.png", alt: "Microsoft" },
  { logo: "previous/planetinnovation.png", alt: "Planet Innovation" },
  { logo: "previous/redhat.png", alt: "Red Hat" },
];
