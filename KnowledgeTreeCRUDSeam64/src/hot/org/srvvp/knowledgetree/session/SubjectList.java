package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("subjectList")
public class SubjectList extends EntityQuery<Subject> {

	private static final String EJBQL = "select subject from Subject subject";

	private static final String[] RESTRICTIONS = {
			"lower(subject.id) like lower(concat(#{subjectList.subject.id},'%'))",
			"lower(subject.description) like lower(concat(#{subjectList.subject.description},'%'))",
			"lower(subject.name) like lower(concat(#{subjectList.subject.name},'%'))",};

	private Subject subject = new Subject();

	public SubjectList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Subject getSubject() {
		return subject;
	}
}
