package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("languageList")
public class LanguageList extends EntityQuery<Language> {

	private static final String EJBQL = "select language from Language language";

	private static final String[] RESTRICTIONS = {
			"lower(language.id) like lower(concat(#{languageList.language.id},'%'))",
			"lower(language.name) like lower(concat(#{languageList.language.name},'%'))",};

	private Language language = new Language();

	public LanguageList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public Language getLanguage() {
		return language;
	}
}
