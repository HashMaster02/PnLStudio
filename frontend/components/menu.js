import { refreshDb } from '@/data/refresh';

const Menu = () => {
	return (
		<header className="border-b-2 font-inter">
			<menu className="container mx-auto px-4 py-2">
				<ul className="max-w-fit flex gap-4">
					<li
						className="py-2 rounded-lg hover:text-red-600 cursor-pointer"
						onClick={() => refreshDb()}
					>
						Refresh Data
					</li>
				</ul>
			</menu>
		</header>
	);
};

export default Menu;
