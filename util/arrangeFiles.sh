if [[ $# -eq 0 ]]; then
    echo "specify 'Pos0' directory" 
else
    zopt=0
    if [ $1 = '-z' -a ! -d $2 -a $2 -ge 1 ]; then
        zopt=$2
        zmode=$3
        1=$zmode
    elif [[ ! -d $1 ]]; then
        echo "follow format 'arngfile_ecoli (-z #) Pos0dir' "
        exit
    fi
    dir405=$1/'405'
    dir488=$1/'488'
    dirPhase=$1/'BF'
    echo 'make directory '$dir405'...'
    mkdir -p $dir405
    if [ $? -eq 0 ];then
        echo 'done'
    else
        exit
    fi
    
    echo 'make directory '$dir488'...'
    mkdir -p $dir488
    if [ $? -eq 0 ];then
        echo 'done'
    else
        exit
    fi
    
    echo 'make directory '$dirPhase'...'
    mkdir -p $dirPhase
    if [ $? -eq 0 ];then
        echo 'done'
    else
        exit
    fi
    
    if [[ zopt -ne 0 ]];then       
        for j in `seq $zopt`;do
            zname=zstack_$j
            zstk405=$dir405/$zname
            zstk488=$dir488/$zname
            zstkPhase=$dirPhase/$zname
            echo 'make directory '$zstk405'...'
            mkdir -p $zstk405
            if [ $? -eq 0 ];then
                echo 'done'
            else
                exit
            fi
            echo 'make directory '$zstk488'...'
            mkdir -p $zstk488
            if [ $? -eq 0 ];then
                echo 'done'
            else
                exit
            fi
            echo 'make directory '$zstkPhase'...'
            mkdir -p $zstkPhase
            if [ $? -eq 0 ];then
                echo 'done'
            else
                exit
            fi
        done
        echo 'finished making z-stack directory...'
    fi
    if [[ zopt -eq 0 ]]; then
        for i in `ls $1 | grep 405`;do
            if [ $i != '405' ];then
                mv $1/$i $dir405
            fi
        done
        
        for i in `ls $1 | grep 488`;do
            if [ $i != '488' ];then
                mv $1/$i $dir488
            fi
        done
        
        for i in `ls $1 | grep Phase`;do
            if [ $i != 'BF' ];then
                mv $1/$i $dirPhase
            fi
        done
        
    else
        echo 'moving images to z-stack directory...'
        echo 'moving 405 images to z-stack directory...'
        for i in `ls $1 | grep 405`;do
            if [ $i != '405' ];then
                for k in `seq $zopt`;do
                    file_number=`basename $i:r | awk -F _ '{print substr($4,3)}'`
                    if [[ $file_number -eq $(( $k - 1 )) ]];then
                        stkfile_405=$dir405/zstack_$k
                        mv $1/$i $stkfile_405
                    fi
                done
            fi
        done
        if [ $? -eq 0 ];then
            echo 'done'
        else
            exit
        fi
        
        echo 'moving 488 images to z-stack directory...'
        for i in `ls $1 | grep 488`;do
            if [ $i != '488' ];then
                for k in `seq $zopt`;do
                    file_number=`basename $i:r | awk -F _ '{print substr($4,3)}'`
                    if [[ $file_number -eq $(( $k - 1 )) ]];then
                        stkfile_488=$dir488/zstack_$k
                        mv $1/$i $stkfile_488
                    fi
                done
            fi
        done
        if [ $? -eq 0 ];then
            echo 'done'
        else
            exit
        fi
        
        echo 'moving Phase images to z-stack directory...'        
        for i in `ls $1 | grep Phase`;do
            if [ $i != 'BF' ];then
                for k in `seq $zopt`;do
                    file_number=`basename $i:r | awk -F _ '{print substr($4,3)}'`
                    if [[ $file_number -eq $(( $k - 1 )) ]];then
                        stkfile_Phase=$dirPhase/zstack_$k
                        mv $1/$i $stkfile_Phase
                    fi
                done
            fi
        done
        if [ $? -eq 0 ];then
            echo 'done'
        else
            exit
        fi
    fi
fi
if [ $? -eq 0 ];then
    echo 'finished all'
else
    exit
fi

