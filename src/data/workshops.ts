export interface Workshop {
  location: string;
  date: string;
  description: string;
  time?: string;
  rsvpUrl?: string;
}

export const workshops: Workshop[] = [
  {
    location: "Online",
    date: "19 February",
    time: "6pm - 7pm AEDT",
    description: "Hosted by PyCon AU via **Python Australia Community Server** on discord. Join us online for a hands-on remote workshop."
  },
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
    location: "Melbourne",
    date: "TBA Mid March",
    description: "Details to be announced soon."
  },
  {
    location: "Online",
    date: "TBA Mid March",
    description: "Hosted by PyCon AU via **Python Australia Community Server** on discord. Join us online for a hands-on remote workshop."
  },
  {
    location: "Brisbane",
    date: "26 March",
    description: "Hosted by the local **Brisbane Python** community."
  },
];
