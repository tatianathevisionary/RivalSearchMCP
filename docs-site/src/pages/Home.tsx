import Hero from '../components/home/Hero'
import ToolsGrid from '../components/home/ToolsGrid'
import BeforeAfter from '../components/home/BeforeAfter'
import QuickSetup from '../components/home/QuickSetup'

export default function Home() {
    return (
        <div>
            <Hero />
            <ToolsGrid />
            <BeforeAfter />
            <QuickSetup />
        </div>
    )
}
