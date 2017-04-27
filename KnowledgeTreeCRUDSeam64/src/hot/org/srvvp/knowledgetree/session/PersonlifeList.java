package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personlifeList")
public class PersonlifeList extends EntityQuery<Personlife> {

	private static final String EJBQL = "select personlife from Personlife personlife";

	private static final String[] RESTRICTIONS = {
			"lower(personlife.id) like lower(concat(#{personlifeList.personlife.id},'%'))",
			"lower(personlife.history) like lower(concat(#{personlifeList.personlife.history},'%'))",
			"lower(personlife.life) like lower(concat(#{personlifeList.personlife.life},'%'))",
			"lower(personlife.period) like lower(concat(#{personlifeList.personlife.period},'%'))",};

	private Personlife personlife = new Personlife();

	public PersonlifeList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Personlife getPersonlife() {
		return personlife;
	}
}
