import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ArrowUpDown, Shield, Users, Zap, TrendingUp, Star, ChevronRight } from 'lucide-react'
import logo from './assets/logo.png'
import './App.css'

// Header Component
function Header() {
  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-border sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <img src={logo} alt="Toolmoon" className="h-10 w-10" />
          <h1 className="text-2xl font-bold text-primary">Toolmoon</h1>
        </div>
        <nav className="hidden md:flex items-center space-x-6">
          <a href="#" className="text-foreground hover:text-primary transition-colors">Trade</a>
          <a href="#" className="text-foreground hover:text-primary transition-colors">Markets</a>
          <a href="#" className="text-foreground hover:text-primary transition-colors">Wallet</a>
          <a href="#" className="text-foreground hover:text-primary transition-colors">Help</a>
        </nav>
        <div className="flex items-center space-x-3">
          <Button variant="outline">Login</Button>
          <Button>Sign Up</Button>
        </div>
      </div>
    </header>
  )
}

// Hero Section
function HeroSection() {
  return (
    <section className="bg-gradient-to-br from-primary/5 via-accent/5 to-background py-20">
      <div className="container mx-auto px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-5xl md:text-6xl font-bold text-foreground mb-6">
            Trade Crypto <span className="text-primary">Peer-to-Peer</span>
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Secure, fast, and decentralized cryptocurrency exchange. Trade directly with other users using your preferred payment methods.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="text-lg px-8 py-6">
              Start Trading <ChevronRight className="ml-2 h-5 w-5" />
            </Button>
            <Button variant="outline" size="lg" className="text-lg px-8 py-6">
              View Markets
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}

// Features Section
function FeaturesSection() {
  const features = [
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Secure Escrow",
      description: "Your funds are protected with our advanced escrow system until trade completion."
    },
    {
      icon: <Users className="h-8 w-8" />,
      title: "P2P Trading",
      description: "Trade directly with other users without intermediaries for better rates."
    },
    {
      icon: <Zap className="h-8 w-8" />,
      title: "Fast Transactions",
      description: "Complete trades quickly with instant notifications and real-time updates."
    },
    {
      icon: <TrendingUp className="h-8 w-8" />,
      title: "Best Rates",
      description: "Get competitive exchange rates from a global network of traders."
    }
  ]

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h3 className="text-4xl font-bold text-foreground mb-4">Why Choose Toolmoon?</h3>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Experience the future of cryptocurrency trading with our innovative P2P platform
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full text-primary w-fit">
                  {feature.icon}
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

// Market Overview Section
function MarketSection() {
  const markets = [
    { pair: "BTC/USD", price: "$67,234", change: "+2.4%", volume: "$2.1M" },
    { pair: "ETH/USD", price: "$3,456", change: "+1.8%", volume: "$1.8M" },
    { pair: "USDT/USD", price: "$1.00", change: "+0.1%", volume: "$5.2M" },
    { pair: "BNB/USD", price: "$432", change: "-0.5%", volume: "$890K" }
  ]

  return (
    <section className="py-20 bg-card">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h3 className="text-4xl font-bold text-foreground mb-4">Live Markets</h3>
          <p className="text-xl text-muted-foreground">
            Real-time cryptocurrency prices and trading volumes
          </p>
        </div>
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ArrowUpDown className="h-5 w-5" />
                Trading Pairs
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {markets.map((market, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-background rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="font-semibold text-lg">{market.pair}</div>
                      <Badge variant={market.change.startsWith('+') ? 'default' : 'destructive'}>
                        {market.change}
                      </Badge>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-lg">{market.price}</div>
                      <div className="text-sm text-muted-foreground">Vol: {market.volume}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

// Stats Section
function StatsSection() {
  const stats = [
    { label: "Total Trades", value: "50,000+", icon: <ArrowUpDown className="h-6 w-6" /> },
    { label: "Active Users", value: "25,000+", icon: <Users className="h-6 w-6" /> },
    { label: "Countries", value: "150+", icon: <TrendingUp className="h-6 w-6" /> },
    { label: "Trust Score", value: "4.9/5", icon: <Star className="h-6 w-6" /> }
  ]

  return (
    <section className="py-20 bg-primary/5">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full text-primary w-fit">
                {stat.icon}
              </div>
              <div className="text-3xl font-bold text-foreground mb-2">{stat.value}</div>
              <div className="text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

// Footer
function Footer() {
  return (
    <footer className="bg-card border-t border-border py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <img src={logo} alt="Toolmoon" className="h-8 w-8" />
              <h4 className="text-xl font-bold text-primary">Toolmoon</h4>
            </div>
            <p className="text-muted-foreground">
              The most trusted P2P cryptocurrency exchange platform.
            </p>
          </div>
          <div>
            <h5 className="font-semibold text-foreground mb-4">Trading</h5>
            <ul className="space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Buy Bitcoin</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Sell Bitcoin</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Buy Ethereum</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Sell Ethereum</a></li>
            </ul>
          </div>
          <div>
            <h5 className="font-semibold text-foreground mb-4">Support</h5>
            <ul className="space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Help Center</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Contact Us</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">FAQ</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Security</a></li>
            </ul>
          </div>
          <div>
            <h5 className="font-semibold text-foreground mb-4">Company</h5>
            <ul className="space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Careers</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-border mt-8 pt-8 text-center text-muted-foreground">
          <p>&copy; 2025 Toolmoon. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

// Main App Component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header />
        <main>
          <HeroSection />
          <FeaturesSection />
          <MarketSection />
          <StatsSection />
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App

                             
