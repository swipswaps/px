# Cross Functional Process Explorer

# Vision
One utility, supporting at least OS X and Linux, replacing
* :white_check_mark: `ps`, but with sensible defaults (just do `px`)
* :white_check_mark: `pgrep` (running `px root` lists only root's processes,
running `px java` lists only java processes)
* :white_check_mark: `pstree` (running `px 1234` shows PID 1234 in a tree, plus
other information about that process)
* :white_check_mark: `top` (by running `px --top`)
* Possibly `iotop`

# Demo
![Screenshot](https://raw.githubusercontent.com/walles/px/python/screenshot.png)

This screenshot shows:
* The end of the output from just typing `px`. Note how the newest and the most
CPU and memory hungry processes are at the end of the list so you can find them
without scrolling.
* The result of searching for "terminal" processes.
* The output from the details view of PID 699:
  * The command line has been split with one argument per line. This makes long
  command lines readable.
  * The process tree shows how the Terminal relates to other processes.
  * Details on how long ago Terminal was started, and how much CPU it has been
  using since.
  * A list of other processes started around the same time as Terminal.
  * The IPC section shows that the Terminal is talking to `launchd` and
  `syslogd` using
  [Unix domain sockets](https://en.wikipedia.org/wiki/Unix_domain_socket).

# Installation
* Go to the [Releases](https://github.com/walles/px/releases) page and download
`px.pex` from there. That file is the whole distribution and can be run as it
is on any Python 2.7 equipped system.
* `sudo install px.pex /usr/local/bin/px`

Now, you should be able to run `px` or `px --help` from the command line.
Otherwise please verify that `/usr/local/bin` is in your `$PATH`.

# Usage
Just type `px`, that's a good start!

Also try `px --help` to see what else `px` can do except for just listing all
processes.

# Development
* Clone: `git clone git@github.com:walles/px.git ; cd px`
* Test: `./ci.sh`
* Build: `./pants binary px`. Your distributable binary is now in `dist/px.pex`.
* Run: `./dist/px.pex`
* To run without first doing the build step: `./pants run px`
* To add dependencies, edit `px/requirements.txt` and `px/BUILD`

# Releasing a new Version
1. Consider updating `screenshot.png` and [the Demo section in this
document](#demo), push those changes.
2. Do `git tag` and think about what the next version number should be.
3. Do ```git tag --annotate 1.2.3``` to set the next version number. The
text you write for this tag will show up as the release description on Github,
write something nice! And remember that the first line is the subject line for
the release.
4. `./pants binary px && ./dist/px.pex --version`, verify that the version
number matches what you just set.
5. `git push --tags`
6. Go to the [Releases](https://github.com/walles/px/releases) page on GitHub,
click your new release, click the `Edit tag` button, then attach your `px.pex`
file that you just built to the release.

# TODO `top` replacement
* Disable terminal line wrapping for smoother handling of terminal window
resizes.
* Print system load before the process listing. Make sure it's really obvious
which number is which if we print all three, maybe a graph of some kind? Maybe
using unicode braille characters like [vtop](https://github.com/MrRio/vtop)?
* On pressing "q" to exit, maybe redraw the screen one last time with a few less
rows than usual before exiting? This way, the top of the view won't scroll out
of sight when the prompt is printed after exiting.
* If the user launches `px` through a symlink that's called something ending in
`top`, enter `top` mode.

# TODO `iotop` replacement
* When given the `--top` flag and enough permissions, record per process IO
usage and present that in one or more columns.

# DONE
* Make `px` list all processes with PID, owner, memory usage (in % of available
RAM), used CPU time, full command line
* Output should be in table format just like `top` or `ps`.
* Output should be truncated at the rightmost column of the terminal window
* Output should be sorted by `score`, with `score` being `(used CPU time) *
(memory usage)`. The intention here is to put the most interesting processes on
top.
* Each column should be wide enough to fit its widest value
* Add a section about installation instructions to this document.
* Add making-a-release instructions to this document
* Add a `.travis.yml` config to the project that:
  * OK: Runs `flake8` on the code
  * OK: Tests the code on OS X
  * OK: Tests the code on Linux
* When piping to some other command, don't truncate lines to terminal width
* If we get one command line argument, only show processes matching that string
as either a user or the name of an executable.
* If we get something looking like a PID as a command line argument, show that
PID process in a tree with all parents up to the top and all children down. This
would replace `pstree`.
* If we get something looking like a PID as a command line argument, for that
PID show:
 * A list of all open files, pipes and sockets
 * For each pipe / domain socket, print the process at the other end
 * For each socket, print where it's going
* Doing `px --version` prints a `git describe` version string.
* Add a column with the name of each running process
* Put column headings at the top of each column
* In the details view, list processes as `Name(PID)` rather than `PID:Name`.
To humans the name is more important than the PID, so it should be first.
* In the details view, list a number of processes that were created around the
same time as the one we're currently looking at.
* Implement support for `px --top`
