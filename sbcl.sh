#!/bin/sh

if [ ! -f /usr/share/common-lisp/source/common-lisp-controller/common-lisp-controller.lisp ] ; then
  cat <<EOF
OF
$0: cannot find the common-lisp-controller source.
EOF
  exit 0
fi

build_error()
{
    echo "Build failure $1"
    exit 1
}

if [ -f /etc/sbcl.rc ] ; then
  RCFILE=/etc/sbcl.rc
else
  RCFILE=/dev/null
fi

case $1 in
    install-clc)
    echo $0 loading and dumping clc.
    ( cd /usr/lib/sbcl
         /usr/bin/sbcl \
           --noinform --disable-ldb --disable-debugger \
           --core /usr/lib/sbcl/sbcl-dist.core \
	   --sysinit ${RCFILE} --no-userinit \
	   --load "/usr/lib/sbcl/install-clc.lisp" # 2> /dev/null
              (mv sbcl-new.core sbcl.core && touch sbcl.core --reference=sbcl-dist.core ) || (echo FAILED ; cp -a sbcl-dist.core sbcl.core ) )
    ;;
    remove-clc)
    echo $0 removing clc-enabled image
    cp -a /usr/lib/sbcl/sbcl-dist.core /usr/lib/sbcl/sbcl.core
    ;;
    rebuild)
    echo $0 rebuilding...
    shift
    echo rebuilding $1
    /usr/bin/sbcl \
             --noinform --disable-ldb --disable-debugger \
             --sysinit ${RCFILE} --no-userinit \
             --eval \
"(handler-case
     (progn
       (asdf:operate 'asdf:compile-op (quote $1))
       (sb-unix:unix-exit 0))
    (error (e)
      (ignore-errors (format t \"~&Build error: ~A~%\" e))
      (finish-output)
      (sb-unix:unix-exit 1)))" || build_error
    ;;
     remove)
    echo $0 removing packages...
    shift
    while [ ! -z "$1" ] ; do
rm -rf "/var/cache/common-lisp-controller/*/sbcl/${1}"
shift
     done
    ;;
    *)
    echo $0 unkown command $1
    echo known commands: rebuild, remove, install-clc, and remove-clc
    exit 1
    ;;
esac

exit 0
