import sys
from typing import List, Union, Optional
from rich.console import Console
from rich.live import Live

#checking type
try:
    import tty
    import termios
    IS_WINDOWS = False
except ImportError:
    import msvcrt
    IS_WINDOWS = True

console = Console()


class DynamicSelectorUI:


    @staticmethod
    def capture_keystroke() -> str:
        #as the function name, i dont want to explain ts
        if IS_WINDOWS:
            ch = msvcrt.getch()

            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                if ch2 == b'H': return 'up'
                if ch2 == b'P': return 'down'
            if ch == b'\r': return 'enter'
            try:
                return ch.decode('utf-8').lower()
            except UnicodeDecodeError:
                return ''
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd) 
            try:
                tty.setraw(fd)                  
                ch = sys.stdin.read(1)         
                if ch == '\x1b':                 
                    ch += sys.stdin.read(2)      
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
                
            if ch == '\x1b[A': return 'up'
            if ch == '\x1b[B': return 'down'
            if ch in ('\r', '\n'): return 'enter'
            return ch.lower()

    def __init__(self, title: str, items: List[str], current_active: Optional[str] = None) -> None:

        self.title: str = title
        self.items: List[str] = items
        self.current_active: Optional[str] = current_active
        

        self.selected_idx: int = items.index(current_active) if current_active in items else 0

    def build_menu_string(self) -> str:

        output_buffer = [f"[bold red]♦  {self.title}[/bold red]"]
        
        for idx, item in enumerate(self.items):
            is_cursor = (idx == self.selected_idx)
            indicator = "[bold green]●[/bold green]" if is_cursor else "[dim white]○[/dim white]"
            text_style = "bold white" if is_cursor else "dim white"
            
            active_annotation = ""
            if self.current_active and item == self.current_active:
                active_annotation = " [dim green](Active Target Profile)[/dim green]"
                
            output_buffer.append(
                f" [bold blue]│[/bold blue] {indicator} [{text_style}]{item}[/{text_style}]{active_annotation}"
            )
            
        return "\n".join(output_buffer)

    def prompt(self, return_index: bool = False) -> Union[str, int, None]:

        if not self.items:
            return None
            
        with Live(self.build_menu_string(), refresh_per_second=20, auto_refresh=False) as live:
            while True:
                live.update(self.build_menu_string(), refresh=True)
                action = self.capture_keystroke()
                
                if action in ('up', 'k') and self.selected_idx > 0:
                    self.selected_idx -= 1
                elif action in ('down', 'j') and self.selected_idx < len(self.items) - 1:
                    self.selected_idx += 1
                elif action == 'enter':
                    return self.selected_idx if return_index else self.items[self.selected_idx]
                elif action in ('\x03', 'q'): #quit
                    return -1 if return_index else None


def selection(title: str, items: List[str], current_active: Optional[str] = None) -> Optional[str]:

    ui = DynamicSelectorUI(title, items, current_active)
    return ui.prompt(return_index=False)