import React from "react";
import Image from "next/image";

const navLinks = [
	{
		href: "/",
		label: "Dashboard",
		icon: (
			<svg
				className="w-6 h-6"
				fill="none"
				stroke="currentColor"
				strokeWidth="2"
				viewBox="0 0 24 24"
			>
				<path
					strokeLinecap="round"
					strokeLinejoin="round"
					d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8v-10h-8v10zm0-18v6h8V3h-8z"
				/>
			</svg>
		),
	},
];

const Navbar = () => {
	return (
		<nav className="hidden md:fixed md:inset-y-0 md:left-0 md:w-64 md:flex md:flex-col bg-card shadow-2xl py-6 px-3 z-40 border-r border-border">
			<div className="flex flex-col items-center mb-8 px-2">
				<Image
					src="/transparent-logo.svg"
					alt="Good Karma Logo"
					width={120}
					height={120}
					className="mb-1"
					priority
					style={{ filter: "drop-shadow(0 0 10px var(--navbar-logo-shadow))" }}
				/>
			</div>
			<hr className="w-4/5 border-t border-border mb-4 mx-auto opacity-70" />
			<ul className="flex flex-col gap-1">
				{navLinks.map((link) => (
					<li key={link.href}>
						<a
							href={link.href}
							className="flex items-center gap-4 px-4 py-3 rounded-md text-base font-medium text-navbar-link hover:bg-orange/15 hover:text-orange transition-colors relative overflow-hidden group focus:bg-orange/20 focus:outline-none"
						>
							{React.cloneElement(link.icon, {
								className:
									"w-6 h-6 text-orange group-hover:text-orange transition-colors",
							})}
							<span>{link.label}</span>
							{/* Ripple effect */}
							<span className="absolute inset-0 group-active:bg-orange/10 transition duration-200 pointer-events-none" />
						</a>
					</li>
				))}
			</ul>
			<div className="mt-auto flex flex-col items-center text-xs text-gray gap-1 pt-10 select-none">
				<span>&copy; 2025 Good Karma</span>
			</div>
		</nav>
	);
};

export default Navbar;
