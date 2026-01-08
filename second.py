import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class TodoItem:
	def __init__(self, id: int, title: str, done: bool = False, created: Optional[str] = None):
		self.id = id
		self.title = title
		self.done = done
		self.created = created or datetime.now().isoformat()

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"title": self.title,
			"done": self.done,
			"created": self.created,
		}

	@staticmethod
	def from_dict(d: dict) -> "TodoItem":
		return TodoItem(d["id"], d["title"], d.get("done", False), d.get("created"))


class TodoList:
	def __init__(self, filename: str = "todos.json"):
		self.filename = Path(filename)
		self.items: List[TodoItem] = []
		self.load()

	def _next_id(self) -> int:
		if not self.items:
			return 1
		return max(i.id for i in self.items) + 1

	def add(self, title: str) -> TodoItem:
		item = TodoItem(self._next_id(), title)
		self.items.append(item)
		return item

	def list(self) -> List[TodoItem]:
		return list(self.items)

	def complete(self, id: int) -> bool:
		for it in self.items:
			if it.id == id:
				it.done = True
				return True
		return False

	def remove(self, id: int) -> bool:
		for i, it in enumerate(self.items):
			if it.id == id:
				del self.items[i]
				return True
		return False

	def save(self) -> None:
		data = [it.to_dict() for it in self.items]
		with self.filename.open("w", encoding="utf-8") as f:
			json.dump(data, f, indent=2)

	def load(self) -> None:
		if not self.filename.exists():
			self.items = []
			return
		try:
			with self.filename.open("r", encoding="utf-8") as f:
				data = json.load(f)
			self.items = [TodoItem.from_dict(d) for d in data]
		except Exception:
			self.items = []


def _print_items(items: List[TodoItem]) -> None:
	if not items:
		print("(no todos)")
		return
	for it in items:
		status = "x" if it.done else " "
		print(f"{it.id:3d}. [{status}] {it.title}")


def interactive_loop(tl: TodoList) -> None:
	print("OOP Todo CLI — type 'help' for commands")
	while True:
		try:
			line = input("> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not line:
			continue
		parts = line.split(maxsplit=1)
		cmd = parts[0].lower()
		arg = parts[1] if len(parts) > 1 else ""

		if cmd in ("exit", "quit"):
			tl.save()
			print("Saved. Bye.")
			break
		if cmd == "help":
			print("Commands: add [title], list, done <id>, remove <id>, save, load, exit")
			continue

		if cmd == "add":
			title = arg or input("Title: ").strip()
			if title:
				item = tl.add(title)
				tl.save()
				print(f"Added {item.id}.")
			continue

		if cmd == "list":
			_print_items(tl.list())
			continue

		if cmd in ("done", "complete"):
			if not arg:
				print("Usage: done <id>")
				continue
			try:
				id = int(arg)
			except ValueError:
				print("Invalid id")
				continue
			ok = tl.complete(id)
			if ok:
				tl.save()
				print("Marked done")
			else:
				print("Not found")
			continue

		if cmd == "remove":
			if not arg:
				print("Usage: remove <id>")
				continue
			try:
				id = int(arg)
			except ValueError:
				print("Invalid id")
				continue
			ok = tl.remove(id)
			if ok:
				tl.save()
				print("Removed")
			else:
				print("Not found")
			continue

		if cmd == "save":
			tl.save()
			print("Saved")
			continue

		if cmd == "load":
			tl.load()
			print("Loaded")
			continue

		print("Unknown command. Type 'help'.")


def _run_cmdline(tl: TodoList, argv: List[str]) -> None:
	# Support simple one-shot commands: add/list/done/remove/save/load
	if len(argv) < 2:
		interactive_loop(tl)
		return
	cmd = argv[1].lower()
	if cmd == "add":
		title = " ".join(argv[2:]).strip()
		if not title:
			print("Provide a title: python second.py add Buy milk")
			return
		item = tl.add(title)
		tl.save()
		print(f"Added {item.id}.")
		return
	if cmd == "list":
		_print_items(tl.list())
		return
	if cmd in ("done", "complete") and len(argv) >= 3:
		try:
			id = int(argv[2])
		except ValueError:
			print("Invalid id")
			return
		if tl.complete(id):
			tl.save()
			print("Marked done")
		else:
			print("Not found")
		return
	if cmd == "remove" and len(argv) >= 3:
		try:
			id = int(argv[2])
		except ValueError:
			print("Invalid id")
			return
		if tl.remove(id):
			tl.save()
			print("Removed")
		else:
			print("Not found")
		return
	if cmd == "save":
		tl.save()
		print("Saved")
		return
	if cmd == "load":
		tl.load()
		print("Loaded")
		return

	print("Unknown or malformed command.")


if __name__ == "__main__":
	tl = TodoList()
	_run_cmdline(tl, sys.argv)

