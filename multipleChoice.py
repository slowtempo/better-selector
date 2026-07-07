import sys
from typing import List, Set
from rich.console import Console
from rich.live import Live

# --- OS Detection ---
try:
    import tty
    import termios
    IS_WINDOWS = False
except ImportError:
    import msvcrt
    IS_WINDOWS = True

console = Console()

class MultiSelectorUI:
    def __init__(self, title: str, items: List[str]) -> None:
        self.title = title
        self.items = items
        self.selected_idx = 0
        self.selected_indices: Set[int] = set()

    @staticmethod
    def capture_keystroke() -> str:
        if IS_WINDOWS:
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                if ch2 == b'H': return 'up'
                if ch2 == b'P': return 'down'
            if ch == b'\r': return 'enter'
            if ch == b' ': return ' '
            try: return ch.decode('utf-8').lower()
            except: return ''
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b': ch += sys.stdin.read(2)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            if ch == '\x1b[A': return 'up'
            if ch == '\x1b[B': return 'down'
            if ch in ('\r', '\n'): return 'enter'
            return ch.lower()

    def build_menu_string(self) -> str:
        output_buffer = [f"[bold red]♦ {self.title} [dim](Space: Toggle, Enter: Done)[/dim][/bold red]"]
        
        for idx, item in enumerate(self.items):
            is_cursor = (idx == self.selected_idx)
            is_selected = idx in self.selected_indices
            
            checkbox = "[bold green][x][/bold green]" if is_selected else "[dim white][ ][/dim white]"
            cursor = "[bold blue]❯[/bold blue]" if is_cursor else " "
            text_style = "bold white" if is_cursor else "dim white"
            
            output_buffer.append(f" {cursor} {checkbox} [{text_style}]{item}[/{text_style}]")
            
        return "\n".join(output_buffer)

    def prompt(self) -> List[str]:
        if not self.items: return []
            
        with Live(self.build_menu_string(), refresh_per_second=20, auto_refresh=False) as live:
            while True:
                live.update(self.build_menu_string(), refresh=True)
                action = self.capture_keystroke()
                
                if action in ('up', 'k'):
                    self.selected_idx = (self.selected_idx - 1) % len(self.items)
                elif action in ('down', 'j'):
                    self.selected_idx = (self.selected_idx + 1) % len(self.items)
                elif action == ' ':
                    if self.selected_idx in self.selected_indices:
                        self.selected_indices.remove(self.selected_idx)
                    else:
                        self.selected_indices.add(self.selected_idx)
                elif action == 'enter':
                    return [self.items[i] for i in self.selected_indices]
                elif action in ('\x03', 'q'):
                    return []

def multi_selection(title: str, items: List[str]) -> List[str]:
    return MultiSelectorUI(title, items).prompt()