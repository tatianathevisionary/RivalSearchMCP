import { Navigation } from "./sections/Navigation";
import { Hero } from "./sections/Hero";
import { Stats } from "./sections/Stats";
import { Features } from "./sections/Features";
import { HowItWorks } from "./sections/HowItWorks";
import { Integrations } from "./sections/Integrations";
import { FAQ } from "./sections/FAQ";
import { CallToAction } from "./sections/CallToAction";
import { Footer } from "./sections/Footer";

export function App() {
  return (
    <>
      <Navigation />
      <main>
        <Hero />
        <Stats />
        <Features />
        <HowItWorks />
        <Integrations />
        <FAQ />
        <CallToAction />
      </main>
      <Footer />
    </>
  );
}
