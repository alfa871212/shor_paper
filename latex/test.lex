% \documentclass[preview]{standalone}
% If the image is too large to fit on this documentclass use
\documentclass[draft]{beamer}
% img_width = 12, img_depth = 4
\usepackage[size=custom,height=18,width=12,scale=0.7]{beamerposter}
% instead and customize the height and width (in cm) to fit.
% Large images may run out of memory quickly.
% To fix this use the LuaLaTeX compiler, which dynamically
% allocates memory.
\usepackage[braket, qm]{qcircuit}
\usepackage{amsmath}
\pdfmapfile{+sansmathaccent.map}
% \usepackage[landscape]{geometry}
% Comment out the above line if using the beamer documentclass.
\begin{document}
\begin{equation*}
    \Qcircuit @C=1.0em @R=1.0em @!R {
	 	\lstick{ {q0}_{0} :  } & \qw & \qw & \qw & \qw\\
	 	\lstick{ {q0}_{1} :  } & \qw & \qw & \qw & \qw\\
	 	\lstick{ {q0}_{2} :  } & \qw & \qw & \qw & \qw\\
	 	\lstick{ {q0}_{3} :  } & \qw & \qw & \qw & \qw\\
	 	\lstick{ {q0}_{4} :  } & \multigate{3}{QFT} & \multigate{3}{QFT} & \qw & \qw\\
	 	\lstick{ {q0}_{5} :  } & \ghost{QFT} & \ghost{QFT} & \qw & \qw\\
	 	\lstick{ {q0}_{6} :  } & \ghost{QFT} & \ghost{QFT} & \qw & \qw\\
	 	\lstick{ {q0}_{7} :  } & \ghost{QFT} & \ghost{QFT} & \qw & \qw\\
	 	\lstick{c0_{0}: } & \cw & \cw & \cw & \cw\\
	 	\lstick{c0_{1}: } & \cw & \cw & \cw & \cw\\
	 	\lstick{c0_{2}: } & \cw & \cw & \cw & \cw\\
	 	\lstick{c0_{3}: } & \cw & \cw & \cw & \cw\\
	 }
\end{equation*}

\end{document}