export interface Workshop {
  location: string;
  date: string;
  description: string;
  time?: string;
  rsvpUrl?: string;
}

export const workshops: Workshop[] = [
  {
    location: "Sydney",
    date: "26 February",
    time: "6pm - 7:00pm AEDT",
    description: "Hosted by **Sydney Python Community**.",
    rsvpUrl: "https://luma.com/5plwd5oh"
  },
  {
    location: "Canberra",
    date: "5 March",
    time: "6pm - 7:30pm AEDT",
    description: "With the **Canberra Python User Group** hosted at ANU.",
    rsvpUrl: "https://www.meetup.com/canberra-python-meetup-group/events/313087616/"
  },
  {
    location: "Online",
    date: "12 March",
    time: "6pm - 7pm AEDT",
    description: "Hosted by PyCon AU via **Python Australia Community Server** on discord. Join us online for a hands-on remote workshop.",
    rsvpUrl: "python-australia-discord"
  },
  {
    location: "Melbourne",
    date: "19 March",
    time: "6:45 – 7:45 PM AEDT",
    description: "Hosted by **Melbourne Python**.",
    rsvpUrl: "https://www.meetup.com/en-au/melbourne-python-user-group/events/313646012/"
  },
  {
    location: "Online",
    date: "24 March",
    time: "6pm - 7pm AEDT",
    description: "Hosted by PyCon AU via **Python Australia Community Server** on discord. Join us online for a hands-on remote workshop.",
    rsvpUrl: "python-australia-discord"
  },
  {
    location: "Brisbane",
    date: "26 March",
    time: "6pm - 8:00pm AEST",
    description: "Hosted by the local **Brisbane Python** community.",
    rsvpUrl: "https://luma.com/7h0i45bq"
  },
];
