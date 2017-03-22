# Create camp_doc_lu table for ncga database
# http://dev.mysql.com/doc/refman/5.7/en/create-table.html
# mysql ncga < create_NCCampDocsLU_table.sql

# FIX THIS --> Make 2 tables, 1 for the report type, and do a lookup instead of having a fucking enum colum

DROP TABLE IF EXISTS camp_doc_lu;
#@ _CREATE_TABLE_
CREATE TABLE camp_doc_lu
(
	id				INT NOT NULL AUTO_INCREMENT,
	committee		VARCHAR(128) NOT NULL,
	report_year		YEAR NOT NULL,
	report_type		ENUM('24-Hour Electioneering Communications','48-Hour','Annual','Audit Letter','Campaign Reporter','Candidate Designation of Committee Funds','Candidate Specific Communications','Certification of Inactive Status','Certification of Incorporated Political Committee','Certification of Return to Active Status','Certification of Threshold','Certification of Treasurer','Certification to Close Committee','Contribution from a Business Account Statement','Correspondence Returned Undeliverable or Unclaimed','Declaration of Intent','Deferred Notice','District Attorney Letter','Electioneering Communications Report','Federal Mid Year','Federal Year End','Final','First Quarter','Forgiven Loan Statement','Fourth Quarter','Independent Expenditure Political Committee Certification','Independent Expenditure Report','Independent Expenditure for Registered Committees','Independent Expenditure for non-Committees','Interim','Judicial Qualifying Contributions Report','Loan Proceeds Statement','Mid Year Semi-Annual','Miscellaneous Correspondence','Monthly','Municipal Voter-Owned Election Qualifying Contributions','Non-Compliance Letter','Non-Participating Candidate','Notice of Candidacy','Notice of Termination of Active Status','Notification of Change to Reporting Schedule','Organizational','Other','Paid Penalty Assessment or Forfeiture','Penalty Appeal','Penalty Appeal Decision','Penalty Assessment','Penalty Assessment Letter','Penalty Resolution Agreement Executed','Penalty Resolution Agreement Proposal','Penalty Waiver Letter','Political Party Executive Committee Exempt Sales Plan','Post General','Post Primary','Pre-Election','Pre-Primary','Pre-Referendum','Pre-Runoff','Rescind Letter','Second Quarter','Signed Penalty Waiver Agreement','Special','Statement of Organization','Supplemental Final','Ten-day','Third Quarter','Thirty-day','Thirty-five-day','Twelve-day','Voter-Owned Election Qualifying Contributions','Weekly','Year End Semi-Annual','Penalty Assessment - 30 Days Aged'),
	amend			BOOL,
	rec_date		DATE,
	start_date		DATE, 
	end_date		DATE,
	image_link		VARCHAR(128) NOT NULL,
	data_link		VARCHAR(384),
	PRIMARY KEY (id)
) ENGINE = InnoDB;
#@ _CREATE_TABLE_
