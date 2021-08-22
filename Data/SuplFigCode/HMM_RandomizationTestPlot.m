function RandomizationTestPlot(saveFolder)
%this function plots the results of the randomization test stored in
%structure statOverview

close all

%saveFolder='~/Dropbox/Data/AnalyzedData/FiguresPaper/';
statMatrixSize=[3,2];
pValueAll=nan(10,7);

%colors
axisColor=[83 83 83]/255;
pStarTextSize=9;
linColor=colormap(lines);

figure

maxMaxValue=0;

binEdges=0:0.01:1;
display(statMatrixSize);

root = saveFolder;
fnames = ["ab","ba"];

for ss=1:statMatrixSize(2);
    edgetype = ss;
    fname = strcat(fnames(edgetype),"List.csv");
    ExpFname = strcat("Exp",fnames(edgetype),".csv");    
    numPlotted=0;

    for tt=1:statMatrixSize(1);
        dirPath = fullfile(root,strcat("sample",num2str(tt)),fname)
        statOverview.randomizedDistributionMean{tt,ss} = table2array(readtable(dirPath));
        dirPath = fullfile(root,strcat("sample",num2str(tt)),ExpFname)
        statOverview.meanSimilarity(tt,ss) = table2array(readtable(dirPath));
        data  = statOverview.randomizedDistributionMean{tt,ss};
        expdata = statOverview.meanSimilarity(tt,ss);
        statOverview.pValueMean(tt,ss) = length(data(data<expdata))/length(data)
  
        if ~isempty(statOverview.randomizedDistributionMean{tt,ss})
            
            numPlotted=numPlotted+1;
            subplot(statMatrixSize(1),statMatrixSize(2),ss+(statMatrixSize(1)-numPlotted)*statMatrixSize(2))
            
            h=histogram(statOverview.randomizedDistributionMean{tt,ss},binEdges);            
            set(gca,'XTick',[0 0.5 1.0],'XTickLabel',[0 0.5 1])
            set(gca,'YTick',[0 0.5],'LineWidth',1.0)
           
            
            hold on
            h.FaceColor=linColor(1,:);
            h.EdgeColor='none';
            h.Normalization = 'probability';
            [maxValue,bin]=max(h.Values);
            bin = bin/100;
            
            darkColor=linColor(1,:)-0.2;
            darkColor(darkColor<0)=0;
            
            k=histogram(statOverview.randomizedDistributionMean{tt,ss},binEdges);
            k.Normalization = 'probability';
            k.DisplayStyle='stairs';
            k.EdgeColor=darkColor;
            
            l=line([statOverview.meanSimilarity(tt,ss)   statOverview.meanSimilarity(tt,ss)],[0 maxValue]);
            set(l,'Color',linColor(2,:),'LineWidth',1)
            axis([0.00 1.00 0.00 0.9])
            currPValue=statOverview.pValueMean(tt,ss);
            
            if currPValue>0
                pValueAll(11-numPlotted,ss)=currPValue;
            else
                pValueAll(11-numPlotted,ss)=1E-4;
            end
         
            yOffsetPstar=0.19;
            
            ncurrPValue = 1 - currPValue;
            
            if currPValue<0.001 || ncurrPValue<0.001
                xPoint=(statOverview.meanSimilarity(tt,ss)+0.5)/2;
                t1=text(xPoint,yOffsetPstar,'***','HorizontalAlignment','center');
                set(t1,'Color',axisColor,'FontName','Arial','FontSize',pStarTextSize)
                t2= plot([bin statOverview.meanSimilarity(tt,ss)],[0.18 0.18],'-k','LineWidth',0.25);
            elseif currPValue<0.01 || ncurrPValue<0.01
                xPoint=(statOverview.meanSimilarity(tt,ss)+0.5)/2;
                t1=text(xPoint,yOffsetPstar,'**','HorizontalAlignment','center');
                set(t1,'Color',axisColor,'FontName','Arial','FontSize',pStarTextSize)
                plot([bin statOverview.meanSimilarity(tt,ss)],[0.18 0.18],'-k','LineWidth',0.25)
            elseif currPValue<0.05 || ncurrPValue<0.05 
                xPoint=(statOverview.meanSimilarity(tt,ss)+0.5)/2;
                t1=text(xPoint,yOffsetPstar,'*','HorizontalAlignment','center');
                set(t1,'Color',axisColor,'FontName','Arial','FontSize',pStarTextSize)
                plot([bin statOverview.meanSimilarity(tt,ss)],[0.18 0.18],'-k','LineWidth',0.25)
            end
            
            set(gca,'LineWidth',0.25)
            set(gca,'box','off')
            if numPlotted>1
                set(gca,'XTick',[0 0.5 1.0],'XTickLabel',{''})
            else
                set(gca,'XTick',[0 0.5 1.0],'XTickLabel',[0 0.5 1])
                xlabel(fnames(edgetype))
            end
            if ss>1
                set(gca,'YTick',[0 0.5],'YTickLabel',{''})
            else
                set(gca,'YTick',[0 0.5],'YTickLabel',[0 0.5])
            end
            maxMaxValue=max(maxValue,maxMaxValue);
        end
    end
end


format='pdf';
paperUnitCurr=get(gcf,'PaperUnits');
height=50;
width=50;
set(gca,'FontName','Arial','LabelFontSizeMultiplier',1)
set(gcf,'Units','centimeters','PaperUnits','centimeters')
set(gcf,'PaperPosition',[0 0 width height],'PaperSize',[width height])
saveName=fullfile(saveFolder,'EdgeRandoTest');
print(saveName,strcat('-d',format),'-r1200');
set(gcf,'PaperUnits',paperUnitCurr)
